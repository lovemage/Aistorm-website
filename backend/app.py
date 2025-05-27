from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import os
from datetime import datetime
from functools import wraps
from database import db, init_db, SiteSettings, Product, User

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app) # 允许所有来源的跨域请求，生产环境中应配置得更严格

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

@app.route('/')
def serve_index():
    # 指向位于项目根目录的 index.html
    from flask import send_from_directory
    return send_from_directory(PROJECT_ROOT, 'index.html')

@app.route('/<path:filename>')
def serve_static_from_root(filename):
    # 服务项目根目录下的静态文件 (例如 assets/, pages/)
    # 需要小心处理，避免暴露不想公开的文件
    # 通常 images, css, js 是安全的
    from flask import send_from_directory
    if filename.startswith('assets/') or filename.startswith('pages/') or filename.endswith('.css') or filename.endswith('.js') or filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.gif'):
        return send_from_directory(PROJECT_ROOT, filename)
    # 对于其他 HTML 文件，如果它们在 pages/ 目录下
    if filename.startswith('pages/') and filename.endswith('.html'):
         return send_from_directory(PROJECT_ROOT, filename)
    return "File not found", 404


if __name__ == '__main__':
    with app.app_context(): #确保在应用上下文中执行
        init_db(app) # 初始化数据库和表
    
    # 获取端口号，支持环境变量
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port) 