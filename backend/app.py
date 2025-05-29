from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import os
from datetime import datetime
from functools import wraps
from database import db, init_db, SiteSettings, Product, User

app = Flask(__name__, template_folder='../templates', static_folder='../static')

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
        return True  # 允许所有来源
    
    return origins

# 简化的CORS配置
CORS(app, 
     supports_credentials=True, 
     origins=get_allowed_origins(),
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     expose_headers=["Content-Type"])

# 会话配置
app.secret_key = os.environ.get('SECRET_KEY', 'aistorm-admin-secret-key-change-in-production')  # 生产环境中应使用随机密钥

# 数据库配置
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'aistorm.db')
# 使用项目根目录的 aistorm.db
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'aistorm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
            user.last_login = datetime.utcnow()
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

if __name__ == '__main__':
    with app.app_context(): #确保在应用上下文中执行
        init_db(app) # 初始化数据库和表
    
    # 获取端口号，支持环境变量
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port) 