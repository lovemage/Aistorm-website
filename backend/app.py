from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, make_response
from flask_cors import CORS
import os
import requests
import hmac
import hashlib
import time
import asyncio
from datetime import datetime, timezone
from functools import wraps
import sys

# 导入数据库模块时添加错误处理
try:
    from database import db, init_db, SiteSettings, Product, User, Order
except ImportError as e:
    print(f"❌ 数据库模块导入失败: {e}")
    # 尝试从不同路径导入
    sys.path.append(os.path.dirname(__file__))
    try:
        from database import db, init_db, SiteSettings, Product, User, Order
        print("✅ 成功从当前目录导入数据库模块")
    except ImportError as e2:
        print(f"❌ 最终导入失败: {e2}")
        raise e2

# Telegram Bot 导入 - 直接使用HTTP API
try:
    import requests
    TELEGRAM_AVAILABLE = True
    print("✅ requests 模块导入成功")
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ requests 模块未安装，将跳过 Telegram 通知功能")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
print(f"✅ Flask应用创建成功: {app.name}")

# 动态CORS配置
def get_allowed_origins():
    """根据环境动态获取允许的CORS来源"""
    origins = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://localhost:8080',
        'http://127.0.0.1:8080'
    ]
    
    # 如果设置了环境变量，添加额外的允许来源
    if os.environ.get('ALLOWED_ORIGINS'):
        additional_origins = os.environ.get('ALLOWED_ORIGINS').split(',')
        origins.extend([origin.strip() for origin in additional_origins])
    
    # 在生产环境中，允许所有来源（如果没有特定配置）
    if os.environ.get('FLASK_ENV') == 'production' and not os.environ.get('ALLOWED_ORIGINS'):
        return ["*"]  # 允许所有来源，使用字符串列表而不是布尔值
    
    return origins

# 简化的CORS配置
CORS(app, 
     supports_credentials=True, 
     origins=get_allowed_origins(),
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     expose_headers=["Content-Type"])

# 会话配置
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ===================== Telegram Bot 配置 =====================

# Telegram Bot 配置 - 从环境变量获取，如果没有则使用空值
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
OXAPAY_SECRET_KEY = os.environ.get('OXAPAY_SECRET_KEY')

# 验证必要的环境变量
if not TELEGRAM_BOT_TOKEN:
    print("⚠️ TELEGRAM_BOT_TOKEN 环境变量未设置")
if not TELEGRAM_CHAT_ID:
    print("⚠️ TELEGRAM_CHAT_ID 环境变量未设置")
if not OXAPAY_SECRET_KEY:
    print("⚠️ OXAPAY_SECRET_KEY 环境变量未设置")

# 初始化 Telegram Bot
telegram_bot = None
if TELEGRAM_AVAILABLE and TELEGRAM_BOT_TOKEN:
    try:
        telegram_bot = requests.Session()
        print("✅ Telegram Bot 初始化成功")
    except Exception as e:
        print(f"❌ Telegram Bot 初始化失败: {str(e)}")
        telegram_bot = None
else:
    print("ℹ️ Telegram Bot 配置不完整，通知功能将被禁用")

def send_telegram_notification(message, parse_mode='HTML'):
    """
    发送Telegram通知
    """
    if not telegram_bot or not TELEGRAM_CHAT_ID:
        print(f"⚠️ Telegram通知跳过: {message}")
        return False
    
    try:
        # 使用requests直接调用Telegram Bot API
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': parse_mode
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram通知发送成功: {message[:50]}...")
            return True
        else:
            print(f"❌ Telegram通知发送失败: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram通知发送失败: {str(e)}")
        return False

def format_order_notification(order, status_type="payment"):
    """
    格式化订单通知消息
    """
    if status_type == "payment":
        emoji = "💰"
        title = "收到USDT支付！"
        status_text = "支付成功"
    elif status_type == "created":
        emoji = "📝"
        title = "新订单创建"
        status_text = "等待支付"
    else:
        emoji = "📄"
        title = "订单更新"
        status_text = status_type
    
    # 构建消息
    message = f"""
{emoji} <b>{title}</b>

📦 <b>产品：</b>{order.product_name}
🔢 <b>数量：</b>{order.quantity} {order.price_unit}
💵 <b>金额：</b>${order.total_amount_usd} USDT
📧 <b>邮箱：</b>{order.customer_email}
🆔 <b>订单号：</b><code>{order.order_id}</code>
📊 <b>状态：</b>{status_text}
⏰ <b>时间：</b>{order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else 'N/A'}

💳 <b>支付方式：</b>{'USDT支付' if order.payment_method == 'usdt' else '支付宝'}
"""

    if order.oxapay_track_id:
        message += f"🔍 <b>追踪ID：</b><code>{order.oxapay_track_id}</code>\n"
    
    if order.customer_notes:
        message += f"📝 <b>客户备注：</b>{order.customer_notes}\n"
    
    return message.strip()

# 数据库配置
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'aistorm.db')
# 使用项目根目录的 aistorm.db

try:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(PROJECT_ROOT, 'aistorm.db')
    
    print(f"📁 项目根目录: {PROJECT_ROOT}")
    print(f"🗄️ 数据库路径: {db_path}")
    print(f"📁 根目录存在: {os.path.exists(PROJECT_ROOT)}")
    
    # 确保数据库目录存在
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        print(f"📁 创建数据库目录: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"✅ 数据库配置成功: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
except Exception as e:
    print(f"❌ 数据库配置失败: {e}")
    # 如果配置失败，使用当前目录
    fallback_db = os.path.join(os.path.dirname(__file__), 'aistorm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + fallback_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(f"⚠️ 使用备用数据库路径: {fallback_db}")

try:
    db.init_app(app)
    print("✅ 数据库初始化成功")
except Exception as e:
    print(f"❌ 数据库初始化失败: {e}")
    raise e

# 身份验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin or not user.is_active:
            flash('需要管理员权限才能访问此页面', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 登录页面
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('admin/login.html')

# 登出
@app.route('/admin/logout')
def logout():
    session.clear()
    flash('已成功登出', 'success')
    return redirect(url_for('login'))

# 修改密码页面
@app.route('/admin/change-password', methods=['GET', 'POST'])
@admin_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.get(session['user_id'])
        
        if not user.check_password(current_password):
            flash('当前密码错误', 'error')
        elif new_password != confirm_password:
            flash('新密码和确认密码不匹配', 'error')
        elif len(new_password) < 6:
            flash('新密码长度至少为6位', 'error')
        else:
            user.set_password(new_password)
            db.session.commit()
            flash('密码修改成功', 'success')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/change_password.html')

# 在第一次请求前初始化数据库
# @app.before_first_request  # Flask 2.3+ deprecated, use with app.app_context() or cli
# def create_tables():
#     init_db(app)

# API 端点：获取站点设置
@app.route('/api/settings', methods=['GET'])
def get_site_settings():
    settings = SiteSettings.query.first()
    if settings:
        return jsonify(settings.to_dict())
    return jsonify({}), 404 # 如果没有设置，返回空对象或错误

# API 端点：更新站点设置 (仅用于后台)
@app.route('/api/settings/update', methods=['POST'])
def update_site_settings_api():
    data = request.json
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
    
    settings.site_name = data.get('site_name', settings.site_name)
    settings.logo_url = data.get('logo_url', settings.logo_url)
    settings.primary_color = data.get('primary_color', settings.primary_color)
    settings.secondary_color = data.get('secondary_color', settings.secondary_color)
    settings.background_color = data.get('background_color', settings.background_color)
    settings.card_background_color = data.get('card_background_color', settings.card_background_color)
    settings.text_color = data.get('text_color', settings.text_color)
    settings.text_accent_color = data.get('text_accent_color', settings.text_accent_color)
    settings.price_color = data.get('price_color', settings.price_color)
    settings.telegram_contact = data.get('telegram_contact', settings.telegram_contact)
    settings.wechat_contact = data.get('wechat_contact', settings.wechat_contact)
    settings.email_contact = data.get('email_contact', settings.email_contact)
    try:
        settings.usdt_to_cny_rate = float(data.get('usdt_to_cny_rate', settings.usdt_to_cny_rate))
    except (ValueError, TypeError):
        pass #保持原值或记录错误
    settings.default_seo_title = data.get('default_seo_title', settings.default_seo_title)
    settings.default_seo_description = data.get('default_seo_description', settings.default_seo_description)
    settings.default_seo_keywords = data.get('default_seo_keywords', settings.default_seo_keywords)
    
    db.session.commit()
    return jsonify({'message': 'Site settings updated successfully!', 'settings': settings.to_dict()})

# 后台管理页面：站点设置
@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings_page():
    settings = SiteSettings.query.first()
    if not settings: # 如果数据库中还没有设置记录，创建一个默认的
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
        settings = SiteSettings.query.first() # 重新查询以获取ID等

    if request.method == 'POST':
        # 从表单获取数据并更新
        settings.site_name = request.form.get('site_name')
        settings.logo_url = request.form.get('logo_url')
        settings.primary_color = request.form.get('primary_color')
        settings.secondary_color = request.form.get('secondary_color')
        settings.background_color = request.form.get('background_color')
        settings.card_background_color = request.form.get('card_background_color')
        settings.text_color = request.form.get('text_color')
        settings.text_accent_color = request.form.get('text_accent_color')
        settings.price_color = request.form.get('price_color')
        settings.telegram_contact = request.form.get('telegram_contact')
        settings.wechat_contact = request.form.get('wechat_contact')
        settings.email_contact = request.form.get('email_contact')
        try:
            settings.usdt_to_cny_rate = float(request.form.get('usdt_to_cny_rate'))
        except (ValueError, TypeError):
             # 可以添加错误提示或日志
            pass # 保持原值
        settings.default_seo_title = request.form.get('default_seo_title')
        settings.default_seo_description = request.form.get('default_seo_description')
        settings.default_seo_keywords = request.form.get('default_seo_keywords')
        
        db.session.commit()
        # 可以添加一个成功消息 flash('Settings updated successfully!')
        return redirect(url_for('admin_settings_page'))
    
    return render_template('admin/settings.html', settings=settings)

# 后台管理首页
@app.route('/admin', methods=['GET'])
@app.route('/admin/', methods=['GET'])
@admin_required
def admin_dashboard():
    # 获取一些统计信息
    total_products = Product.query.count()
    active_products = Product.query.filter_by(is_active=True).count()
    featured_products = Product.query.filter_by(is_featured=True).count()
    out_of_stock = Product.query.filter_by(in_stock=False).count()
    
    stats = {
        'total_products': total_products,
        'active_products': active_products,
        'featured_products': featured_products,
        'out_of_stock': out_of_stock
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# API 端点：获取所有产品
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.filter_by(is_active=True).order_by(Product.sort_order, Product.id).all()
    return jsonify([product.to_dict() for product in products])

# API 端点：获取特定产品
@app.route('/api/products/<slug>', methods=['GET'])
def get_product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if product:
        return jsonify(product.to_dict())
    return jsonify({'error': 'Product not found'}), 404

# API 端点：创建新产品 (后台使用)
@app.route('/api/products', methods=['POST'])
def create_product():
    import json
    data = request.json
    
    # 检查slug是否已存在
    if Product.query.filter_by(slug=data.get('slug')).first():
        return jsonify({'error': 'Product slug already exists'}), 400
    
    try:
        product = Product(
            name=data.get('name'),
            slug=data.get('slug'),
            description=data.get('description', ''),
            short_description=data.get('short_description', ''),
            price_usd=float(data.get('price_usd', 0)),
            price_unit=data.get('price_unit', '月'),
            image_url=data.get('image_url', ''),
            page_url=data.get('page_url', ''),
            in_stock=data.get('in_stock', True),
            stock_quantity=int(data.get('stock_quantity', 999)),
            is_featured=data.get('is_featured', False),
            is_active=data.get('is_active', True),
            sort_order=int(data.get('sort_order', 0)),
            category=data.get('category', 'AI工具'),
            features=json.dumps(data.get('features', [])),
            seo_title=data.get('seo_title', ''),
            seo_description=data.get('seo_description', ''),
            seo_keywords=data.get('seo_keywords', '')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully!', 'product': product.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API 端点：更新产品 (后台使用)
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    import json
    product = Product.query.get_or_404(product_id)
    data = request.json
    
    try:
        product.name = data.get('name', product.name)
        product.slug = data.get('slug', product.slug)
        product.description = data.get('description', product.description)
        product.short_description = data.get('short_description', product.short_description)
        product.price_usd = float(data.get('price_usd', product.price_usd))
        product.price_unit = data.get('price_unit', product.price_unit)
        product.image_url = data.get('image_url', product.image_url)
        product.page_url = data.get('page_url', product.page_url)
        product.in_stock = data.get('in_stock', product.in_stock)
        product.stock_quantity = int(data.get('stock_quantity', product.stock_quantity))
        product.is_featured = data.get('is_featured', product.is_featured)
        product.is_active = data.get('is_active', product.is_active)
        product.sort_order = int(data.get('sort_order', product.sort_order))
        product.category = data.get('category', product.category)
        product.features = json.dumps(data.get('features', []))
        product.seo_title = data.get('seo_title', product.seo_title)
        product.seo_description = data.get('seo_description', product.seo_description)
        product.seo_keywords = data.get('seo_keywords', product.seo_keywords)
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully!', 'product': product.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API 端点：删除产品 (后台使用)
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully!'})

# API 端点：批量更新产品库存 (后台使用)
@app.route('/api/products/batch-update-stock', methods=['POST', 'OPTIONS'])
def batch_update_stock():
    # 处理 OPTIONS 请求（CORS预检）
    if request.method == 'OPTIONS':
        return '', 200
    
    print(f"Session data in batch_update_stock: {dict(session)}")  # 添加日志
    print(f"Request JSON in batch_update_stock: {request.json}")  # 添加日志
    print(f"Request headers: {dict(request.headers)}")  # 添加请求头日志
    
    # 检查身份验证
    if 'user_id' not in session:
        print("No user_id in session")  # 调试日志
        return jsonify({'success': False, 'error': '未登录，请先登录后台管理系统'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin or not user.is_active:
        print(f"User validation failed: user={user}, is_admin={user.is_admin if user else None}, is_active={user.is_active if user else None}")  # 调试日志
        return jsonify({'success': False, 'error': '需要管理员权限'}), 403
    
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': '请求数据为空'}), 400
            
        updates = data.get('updates', [])
        
        if not updates:
            return jsonify({'success': False, 'error': '没有提供更新数据'}), 400
        
        print(f"Processing {len(updates)} updates")  # 调试日志
        updated_count = 0
        
        for update in updates:
            product_id = update.get('id')
            in_stock = update.get('in_stock', True)
            stock_quantity = update.get('stock_quantity', 0)
            
            if not product_id:
                continue
                
            product = Product.query.get(product_id)
            if product:
                product.in_stock = in_stock
                product.stock_quantity = stock_quantity
                updated_count += 1
                print(f"Updated product {product_id}: in_stock={in_stock}, stock_quantity={stock_quantity}")  # 调试日志
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'updated_count': updated_count,
            'message': f'成功更新了 {updated_count} 个产品的库存信息'
        })
        
    except Exception as e:
        print(f"Exception in batch_update_stock: {str(e)}")  # 调试日志
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'批量更新失败: {str(e)}'
        }), 500

# API 端点：批量更新产品价格 (后台使用)
@app.route('/api/products/batch-update-prices', methods=['POST', 'OPTIONS'])
def batch_update_prices():
    # 处理 OPTIONS 请求（CORS预检）
    if request.method == 'OPTIONS':
        return '', 200
    
    print(f"Session data in batch_update_prices: {dict(session)}")
    print(f"Request JSON in batch_update_prices: {request.json}")
    
    # 检查身份验证
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': '未登录，请先登录后台管理系统'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin or not user.is_active:
        return jsonify({'success': False, 'error': '需要管理员权限'}), 403
    
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': '请求数据为空'}), 400
            
        updates = data.get('updates', [])
        
        if not updates:
            return jsonify({'success': False, 'error': '没有提供更新数据'}), 400
        
        print(f"Processing {len(updates)} price updates")
        updated_count = 0
        
        for update in updates:
            product_id = update.get('id')
            price_usd = update.get('price_usd')
            price_unit = update.get('price_unit')
            
            if not product_id or price_usd is None:
                continue
                
            product = Product.query.get(product_id)
            if product:
                product.price_usd = float(price_usd)
                if price_unit:
                    product.price_unit = price_unit
                updated_count += 1
                print(f"Updated product {product_id}: price_usd={price_usd}, price_unit={price_unit}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'updated_count': updated_count,
            'message': f'成功更新了 {updated_count} 个产品的价格信息'
        })
        
    except Exception as e:
        print(f"Exception in batch_update_prices: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'批量更新价格失败: {str(e)}'
        }), 500

# 后台管理页面：产品管理
@app.route('/admin/products', methods=['GET'])
@admin_required
def admin_products_page():
    products = Product.query.order_by(Product.sort_order, Product.id).all()
    return render_template('admin/products.html', products=products)

# 后台管理页面：编辑产品
@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_product_page(product_id):
    import json
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name')
            product.slug = request.form.get('slug')
            product.description = request.form.get('description')
            product.short_description = request.form.get('short_description')
            product.price_usd = float(request.form.get('price_usd'))
            product.price_unit = request.form.get('price_unit')
            product.image_url = request.form.get('image_url')
            product.page_url = request.form.get('page_url')
            product.in_stock = 'in_stock' in request.form
            product.stock_quantity = int(request.form.get('stock_quantity'))
            product.is_featured = 'is_featured' in request.form
            product.is_active = 'is_active' in request.form
            product.sort_order = int(request.form.get('sort_order'))
            product.category = request.form.get('category')
            
            # 处理特性列表
            features_text = request.form.get('features', '')
            if features_text.strip():
                features_list = [f.strip() for f in features_text.split('\n') if f.strip()]
                product.features = json.dumps(features_list)
            else:
                product.features = json.dumps([])
            
            product.seo_title = request.form.get('seo_title')
            product.seo_description = request.form.get('seo_description')
            product.seo_keywords = request.form.get('seo_keywords')
            
            db.session.commit()
            return redirect(url_for('admin_products_page'))
        except Exception as e:
            # 可以添加错误处理
            pass
    
    # 将features JSON转换为文本格式用于表单显示
    features_text = ''
    if product.features:
        try:
            features_list = json.loads(product.features)
            features_text = '\n'.join(features_list)
        except:
            features_text = ''
    
    return render_template('admin/edit_product.html', product=product, features_text=features_text)

# 后台管理页面：添加新产品
@app.route('/admin/products/new', methods=['GET', 'POST'])
@admin_required
def admin_new_product_page():
    import json
    if request.method == 'POST':
        try:
            # 检查slug是否已存在
            slug = request.form.get('slug')
            if Product.query.filter_by(slug=slug).first():
                # 可以添加错误消息
                return render_template('admin/new_product.html', error='产品标识符已存在')
            
            # 处理特性列表
            features_text = request.form.get('features', '')
            features_list = []
            if features_text.strip():
                features_list = [f.strip() for f in features_text.split('\n') if f.strip()]
            
            product = Product(
                name=request.form.get('name'),
                slug=slug,
                description=request.form.get('description'),
                short_description=request.form.get('short_description'),
                price_usd=float(request.form.get('price_usd')),
                price_unit=request.form.get('price_unit'),
                image_url=request.form.get('image_url'),
                page_url=request.form.get('page_url'),
                in_stock='in_stock' in request.form,
                stock_quantity=int(request.form.get('stock_quantity')),
                is_featured='is_featured' in request.form,
                is_active='is_active' in request.form,
                sort_order=int(request.form.get('sort_order')),
                category=request.form.get('category'),
                features=json.dumps(features_list),
                seo_title=request.form.get('seo_title'),
                seo_description=request.form.get('seo_description'),
                seo_keywords=request.form.get('seo_keywords')
            )
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('admin_products_page'))
        except Exception as e:
            return render_template('admin/new_product.html', error=str(e))
    
    return render_template('admin/new_product.html')

# 首页路由 - 优先级最高
@app.route('/')
def serve_index():
    # 指向位于项目根目录的 index.html
    from flask import send_from_directory
    return send_from_directory(PROJECT_ROOT, 'index.html')

# 静态文件路由 - 处理所有静态资源
@app.route('/<path:filename>')
def serve_static_from_root(filename):
    # 服务项目根目录下的静态文件 (例如 assets/, pages/)
    # 需要小心处理，避免暴露不想公开的文件
    from flask import send_from_directory
    
    # 允许的文件类型和目录
    allowed_extensions = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot')
    allowed_directories = ('assets/', 'pages/')
    
    # 检查是否为允许的静态文件
    if (filename.startswith(allowed_directories) or 
        filename.endswith(allowed_extensions) or
        (filename.startswith('pages/') and filename.endswith('.html')) or
        (filename.startswith('google') and filename.endswith('.html'))):  # 添加对Google验证文件的支持
        try:
            return send_from_directory(PROJECT_ROOT, filename)
        except FileNotFoundError:
            return "File not found", 404
    
    # 对于其他请求，返回404
    return "File not found", 404

# 生成sitemap.xml
@app.route('/sitemap.xml')
def generate_sitemap():
    from flask import Response
    from datetime import datetime
    import xml.etree.ElementTree as ET
    
    # 创建sitemap根元素
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 网站基础URL
    base_url = "https://www.aistorm.art"
    
    # 定义静态页面
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'url': '/pages/about.html', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/pages/faq.html', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/pages/tutorials.html', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': '/pages/support.html', 'priority': '0.6', 'changefreq': 'monthly'},
        {'url': '/pages/privacy.html', 'priority': '0.5', 'changefreq': 'yearly'},
        {'url': '/pages/terms.html', 'priority': '0.5', 'changefreq': 'yearly'},
        {'url': '/pages/refund.html', 'priority': '0.5', 'changefreq': 'yearly'},
    ]
    
    # 产品页面
    product_pages = [
        {'url': '/pages/chatgpt.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pages/claude.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pages/grok.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pages/cursor.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pages/lovable.html', 'priority': '0.9', 'changefreq': 'weekly'},
    ]
    
    # 添加静态页面
    for page in static_pages + product_pages:
        url_elem = ET.SubElement(urlset, "url")
        
        loc = ET.SubElement(url_elem, "loc")
        loc.text = base_url + page['url']
        
        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = current_date
        
        changefreq = ET.SubElement(url_elem, "changefreq")
        changefreq.text = page['changefreq']
        
        priority = ET.SubElement(url_elem, "priority")
        priority.text = page['priority']
    
    # 添加动态产品页面（从数据库获取）
    try:
        products = Product.query.filter_by(is_active=True).all()
        for product in products:
            url_elem = ET.SubElement(urlset, "url")
            
            loc = ET.SubElement(url_elem, "loc")
            # 如果产品有自定义页面URL，使用它；否则使用API端点
            if product.page_url and product.page_url.startswith('pages/'):
                loc.text = base_url + '/' + product.page_url
            else:
                loc.text = base_url + '/api/products/' + product.slug
            
            lastmod = ET.SubElement(url_elem, "lastmod")
            lastmod.text = current_date
            
            changefreq = ET.SubElement(url_elem, "changefreq")
            changefreq.text = "weekly"
            
            priority = ET.SubElement(url_elem, "priority")
            priority.text = "0.8"
    except Exception as e:
        # 如果数据库查询失败，只返回静态页面
        pass
    
    # 生成XML字符串
    xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
    
    # 添加XML声明
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
    
    # 返回XML响应
    return Response(xml_content, mimetype='application/xml')

# 提供robots.txt文件
@app.route('/robots.txt')
def robots_txt():
    from flask import send_from_directory
    try:
        return send_from_directory(PROJECT_ROOT, 'robots.txt')
    except FileNotFoundError:
        # 如果文件不存在，返回基本的robots.txt内容
        from flask import Response
        robots_content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /backend/

Sitemap: https://www.aistorm.art/sitemap.xml
"""
        return Response(robots_content, mimetype='text/plain')

# ===================== 订单管理 API =====================

# API 端点：创建订单
@app.route('/api/create-order', methods=['POST', 'OPTIONS'])
def create_order():
    # 处理 OPTIONS 请求（CORS预检）
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    try:
        # 获取JSON数据并进行错误处理
        if not request.is_json:
            return jsonify({'success': False, 'error': '请求必须是JSON格式'}), 400
        
        try:
            data = request.get_json(force=True)
        except Exception as json_error:
            print(f"JSON解析错误: {str(json_error)}")
            print(f"原始数据: {request.get_data(as_text=True)}")
            return jsonify({'success': False, 'error': f'JSON格式错误: {str(json_error)}'}), 400
        
        if not data:
            return jsonify({'success': False, 'error': '空的请求数据'}), 400

        # 验证必需的字段
        required_fields = ['customer_email', 'product_slug', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'缺少必需字段: {field}'}), 400

        # 查找产品
        product = Product.query.filter_by(slug=data['product_slug']).first()
        if not product:
            return jsonify({'success': False, 'error': '产品不存在'}), 404

        # 检查库存
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'success': False, 'error': '数量必须大于0'}), 400
        
        if product.stock_quantity < quantity:
            return jsonify({'success': False, 'error': '库存不足'}), 400

        # 计算总价
        total_amount = float(product.price_usd) * quantity

        # 生成订单ID
        import time
        order_id = f"order_{int(time.time() * 1000)}_{os.urandom(4).hex()}"

        # 创建订单
        order = Order(
            order_id=order_id,
            customer_email=data['customer_email'],
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            product_id=product.id,
            product_name=product.name,
            quantity=quantity,
            total_amount_usd=total_amount,
            payment_status='pending',
            order_status='created'
        )

        db.session.add(order)
        db.session.commit()

        # 发送订单创建通知
        try:
            notification_message = format_order_notification(order, "create")
            send_telegram_notification(notification_message)
        except Exception as e:
            print(f"发送订单通知失败: {str(e)}")

        return jsonify({
            'success': True,
            'order_id': order_id,
            'total_amount': total_amount,
            'message': '订单创建成功'
        })

    except Exception as e:
        print(f"创建订单错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# API 端点：OxaPay支付请求
@app.route('/api/oxapay-payment', methods=['POST', 'OPTIONS'])
def create_oxapay_payment():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        order_id = data.get('orderId')
        
        # 获取订单信息
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({'success': False, 'error': '订单不存在'}), 404
        
        # OxaPay API配置
        OXAPAY_API_URL = "https://api.oxapay.com/merchants/request"
        OXAPAY_MERCHANT_ID = OXAPAY_SECRET_KEY  # 使用环境变量中的API Key
        
        # 构建回调URL
        callback_url = f"{request.host_url}oxapay-webhook"
        
        # 构建OxaPay请求数据
        oxapay_data = {
            'merchant': OXAPAY_MERCHANT_ID,
            'amount': float(order.total_amount_usd),
            'currency': 'USDT',
            'lifeTime': 15,  # 15分钟过期
            'feePaidByPayer': 1,
            'callbackUrl': callback_url,
            'description': f"购买 {order.product_name} x{order.quantity}",
            'orderId': order.order_id,
            'email': order.customer_email,
        }
        
        # 发送请求到OxaPay
        response = requests.post(OXAPAY_API_URL, json=oxapay_data, timeout=30)
        response_data = response.json()
        
        print(f"OxaPay响应: {response_data}")  # 调试日志
        
        # 检查是否是测试环境 (API密钥无效时)
        if response_data.get('error') == 'Invalid merchant API key' or response_data.get('result') == 102:
            print("⚠️ 检测到无效API密钥，启用测试模式")
            # 返回模拟的支付响应用于测试
            test_response = {
                'result': 100,
                'orderId': f'oxapay_{order.order_id}',
                'trackId': f'track_{int(time.time())}',
                'payLink': f'{request.host_url}test_payment_success.html?order={order.order_id}&amount={order.total_amount_usd}&trackId=track_{int(time.time())}'
            }
            response_data = test_response
            print(f"测试模式响应: {response_data}")
        
        if response_data.get('result') == 100:
            # 更新订单信息
            order.oxapay_order_id = response_data.get('orderId')
            order.oxapay_track_id = response_data.get('trackId')
            order.oxapay_pay_link = response_data.get('payLink')
            order.order_status = 'processing'
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'payLink': response_data.get('payLink'),
                'trackId': response_data.get('trackId'),
                'orderId': response_data.get('orderId'),
                'testMode': 'Invalid merchant API key' in str(response_data)
            })
        else:
            error_msg = response_data.get('message', '生成支付链接失败')
            return jsonify({'success': False, 'error': error_msg}), 400
            
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'OxaPay API请求超时'}), 500
    except Exception as e:
        print(f"OxaPay支付错误: {str(e)}")
        return jsonify({'success': False, 'error': f'生成支付链接失败: {str(e)}'}), 500

# OxaPay Webhook处理
@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    try:
        data = request.json
        print(f"收到OxaPay Webhook: {data}")  # 调试日志
        
        # 获取订单信息
        order_id = data.get('orderId')
        track_id = data.get('trackId')
        status = data.get('status')
        amount = data.get('amount')
        currency = data.get('currency')
        
        if not order_id:
            print("❌ Webhook缺少orderId")
            return jsonify({'error': 'Missing orderId'}), 400
        
        # 验证签名（如果配置了密钥）
        if OXAPAY_SECRET_KEY and data.get('sign'):
            received_sign = data.get('sign', '')
            # 根据OxaPay文档构建签名字符串
            sign_string = f"{order_id}{OXAPAY_SECRET_KEY}"
            calculated_sign = hashlib.sha256(sign_string.encode()).hexdigest()
            
            if received_sign != calculated_sign:
                print(f"❌ 签名验证失败: 收到={received_sign}, 计算={calculated_sign}")
                return jsonify({'error': 'Invalid signature'}), 401
            else:
                print("✅ 签名验证通过")
        else:
            print("ℹ️ 跳过签名验证（测试模式或无签名）")
        
        # 查找订单
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            print(f"❌ 订单不存在: {order_id}")
            return jsonify({'error': 'Order not found'}), 404
        
        # 记录原始状态
        old_payment_status = order.payment_status
        old_order_status = order.order_status
        
        # 更新订单状态
        notification_sent = False
        
        if status == 'Paid' or status == 'Completed':
            order.payment_status = 'completed'
            order.order_status = 'completed'
            order.paid_at = datetime.now(timezone.utc)
            
            # 更新产品库存
            if order.product and order.product.stock_quantity > 0:
                order.product.stock_quantity = max(0, order.product.stock_quantity - order.quantity)
            
            print(f"✅ 订单 {order_id} 支付成功")
            
            # 发送支付成功通知
            try:
                notification_message = format_order_notification(order, "payment")
                # 添加额外的支付信息
                notification_message += f"\n\n💎 <b>OxaPay详情：</b>"
                if track_id:
                    notification_message += f"\n🔍 追踪ID: <code>{track_id}</code>"
                if amount and currency:
                    notification_message += f"\n💰 实收金额: {amount} {currency}"
                
                notification_message += f"\n\n🎉 <b>请及时处理账号交付！</b>"
                
                send_telegram_notification(notification_message)
                notification_sent = True
            except Exception as e:
                print(f"发送支付通知失败: {str(e)}")
            
        elif status == 'Failed' or status == 'Expired':
            order.payment_status = 'failed'
            order.order_status = 'cancelled'
            print(f"❌ 订单 {order_id} 支付失败: {status}")
            
            # 发送支付失败通知
            try:
                fail_message = f"""
❌ <b>支付失败通知</b>

🆔 <b>订单号：</b><code>{order.order_id}</code>
📦 <b>产品：</b>{order.product_name}
💵 <b>金额：</b>${order.total_amount_usd} USDT
📧 <b>邮箱：</b>{order.customer_email}
❗ <b>失败原因：</b>{status}
⏰ <b>时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                send_telegram_notification(fail_message)
                notification_sent = True
            except Exception as e:
                print(f"发送失败通知失败: {str(e)}")
                
        elif status == 'Processing' or status == 'Waiting':
            order.payment_status = 'pending'
            order.order_status = 'processing'
            print(f"⏳ 订单 {order_id} 支付处理中: {status}")
            
        else:
            print(f"⚠️ 未知支付状态: {status}")
        
        # 保存更改
        db.session.commit()
        
        # 如果状态有变化且未发送通知，发送状态更新通知
        if (old_payment_status != order.payment_status or old_order_status != order.order_status) and not notification_sent:
            try:
                status_message = f"""
📄 <b>订单状态更新</b>

🆔 <b>订单号：</b><code>{order.order_id}</code>
📦 <b>产品：</b>{order.product_name}
💵 <b>金额：</b>${order.total_amount_usd} USDT
📊 <b>支付状态：</b>{old_payment_status} → {order.payment_status}
📊 <b>订单状态：</b>{old_order_status} → {order.order_status}
⏰ <b>时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                send_telegram_notification(status_message)
            except Exception as e:
                print(f"发送状态更新通知失败: {str(e)}")
        
        return jsonify({'success': True, 'message': 'Webhook processed successfully'}), 200
        
    except Exception as e:
        print(f"❌ Webhook处理错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API 端点：获取订单状态
@app.route('/api/order-status/<order_id>', methods=['GET'])
def get_order_status(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({'success': False, 'error': '订单不存在'}), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API 端点：测试Telegram通知 (仅用于开发测试)
@app.route('/api/test-telegram', methods=['POST'])
def test_telegram():
    try:
        data = request.json or {}
        message_type = data.get('type', 'test')
        
        if message_type == 'test':
            test_message = f"""
🤖 <b>Telegram Bot 测试消息</b>

⏰ <b>时间：</b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔧 <b>系统：</b>AIStorm 支付系统
✅ <b>状态：</b>通知功能正常

如果您收到此消息，说明 Telegram Bot 配置正确！
"""
        elif message_type == 'config':
            config_info = f"""
⚙️ <b>Telegram Bot 配置信息</b>

🤖 <b>Bot Token：</b>{'已配置' if TELEGRAM_BOT_TOKEN else '未配置'}
💬 <b>Chat ID：</b>{'已配置' if TELEGRAM_CHAT_ID else '未配置'}
🔐 <b>OxaPay Secret：</b>{'已配置' if OXAPAY_SECRET_KEY else '未配置'}
📚 <b>Telegram库：</b>{'可用' if TELEGRAM_AVAILABLE else '未安装'}
🔗 <b>Bot实例：</b>{'已初始化' if telegram_bot else '未初始化'}

配置环境变量:
• TELEGRAM_BOT_TOKEN
• TELEGRAM_CHAT_ID  
• OXAPAY_SECRET_KEY
"""
            test_message = config_info
        else:
            test_message = data.get('message', '这是一条测试消息')
        
        success = send_telegram_notification(test_message)
        
        return jsonify({
            'success': success,
            'message': '测试消息已发送' if success else '测试消息发送失败',
            'bot_configured': telegram_bot is not None,
            'chat_id_configured': bool(TELEGRAM_CHAT_ID)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 测试支付页面路由
@app.route('/test_payment_success.html')
def test_payment_page():
    from flask import send_from_directory
    try:
        return send_from_directory(PROJECT_ROOT, 'test_payment_success.html')
    except FileNotFoundError:
        return "Test payment page not found", 404

if __name__ == '__main__':
    try:
        print("🚀 启动AIStorm应用...")
        print(f"🐍 Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"📁 当前工作目录: {os.getcwd()}")
        print(f"📁 项目根目录: {PROJECT_ROOT}")
        
        with app.app_context(): #确保在应用上下文中执行
            init_db(app) # 初始化数据库和表
        
        # 获取端口号，支持环境变量
        port = int(os.environ.get('PORT', 5001))
        flask_env = os.environ.get('FLASK_ENV', 'development')
        debug = flask_env != 'production'
        
        print(f"🌐 启动配置:")
        print(f"  📍 端口: {port}")
        print(f"  🏭 环境: {flask_env}")
        print(f"  🔧 调试模式: {debug}")
        print(f"  🌍 主机: 0.0.0.0")
        
        app.run(debug=debug, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 