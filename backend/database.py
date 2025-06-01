from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='AIStorm')
    logo_url = db.Column(db.String(200), default='../assets/images/logo.png')
    
    # Color Scheme
    primary_color = db.Column(db.String(7), default='#00E5FF') # 荧光青
    secondary_color = db.Column(db.String(7), default='#D400FF') # 洋红色
    background_color = db.Column(db.String(7), default='#0D0F12') # 深邃背景
    card_background_color = db.Column(db.String(7), default='#1A1D24') # 卡片背景
    text_color = db.Column(db.String(7), default='#EAEAEA') # 主要文字
    text_accent_color = db.Column(db.String(7), default='#00E5FF') # 文字强调色 (可与主色一致)
    price_color = db.Column(db.String(7), default='#39FF14') # 价格颜色 (荧光绿)

    # Contact Information
    telegram_contact = db.Column(db.String(100), default='@aistorm2025')
    wechat_contact = db.Column(db.String(100), default='aistorm2024')
    email_contact = db.Column(db.String(100), default='support@aistorm.com')
    
    # Currency
    usdt_to_cny_rate = db.Column(db.Float, default=8.0)

    # SEO - these might be better managed per-page, but a global default is fine
    default_seo_title = db.Column(db.String(200), default='AIStorm | Your Trusted AI Solutions Provider')
    default_seo_description = db.Column(db.String(500), default='Discover and purchase top AI product accounts like ChatGPT Pro, Claude Max, Super Grok, and more with secure USDT payment.')
    default_seo_keywords = db.Column(db.String(500), default='AI Accounts, ChatGPT, Claude, Grok, AI Tools, USDT Payment')

    def to_dict(self):
        return {
            'site_name': self.site_name,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'background_color': self.background_color,
            'card_background_color': self.card_background_color,
            'text_color': self.text_color,
            'text_accent_color': self.text_accent_color,
            'price_color': self.price_color,
            'telegram_contact': self.telegram_contact,
            'wechat_contact': self.wechat_contact,
            'email_contact': self.email_contact,
            'usdt_to_cny_rate': self.usdt_to_cny_rate,
            'default_seo_title': self.default_seo_title,
            'default_seo_description': self.default_seo_description,
            'default_seo_keywords': self.default_seo_keywords
        }

def init_db(app):
    import json
    with app.app_context():
        db.create_all()
        
        # Create default admin user if no users exist
        if User.query.count() == 0:
            admin_user = User(
                username='admin',
                email='admin@aistorm.com',
                is_active=True,
                is_admin=True
            )
            admin_user.set_password('admin123')  # 默认密码，建议首次登录后修改
            db.session.add(admin_user)
            db.session.commit()
            print("Created default admin user: admin / admin123")
        
        # Create initial settings if they don't exist
        if SiteSettings.query.first() is None:
            default_settings = SiteSettings()
            db.session.add(default_settings)
            db.session.commit()
            print("Initialized database with default site settings.")
        
        # Create initial products if they don't exist
        if Product.query.count() == 0:
            default_products = [
                {
                    'name': 'ChatGPT Pro',
                    'slug': 'chatgpt-pro',
                    'description': '体验 OpenAI 最新的 ChatGPT Pro，享受无限制的 GPT-4 Turbo 访问权限。',
                    'short_description': 'OpenAI 官方 Pro 版本，无限制 GPT-4 Turbo',
                    'price_usd': 130.0,
                    'price_unit': '月',
                    'image_url': 'assets/images/chatgptpro.png',
                    'page_url': 'pages/chatgpt.html',
                    'in_stock': True,
                    'stock_quantity': 50,
                    'is_featured': True,
                    'sort_order': 1,
                    'category': 'AI对话助手',
                    'features': json.dumps([
                        'GPT-4 Turbo 无限制访问',
                        '更快的响应速度',
                        '优先访问新功能',
                        '高峰期优先使用权'
                    ]),
                    'seo_title': '购买 ChatGPT Pro 帐号 - OpenAI 官方 Pro 版本',
                    'seo_description': '购买正版 ChatGPT Pro 帐号，享受 GPT-4 Turbo 无限制访问。AIStorm 提供安全的 USDT 支付。',
                    'seo_keywords': 'ChatGPT Pro, GPT-4 Turbo, OpenAI, AI对话, USDT支付'
                },
                {
                    'name': 'Claude Max 5x',
                    'slug': 'claude-max-5x',
                    'description': '体验 Anthropic 的 Claude Max 5x，享受 5 倍使用量的强大 AI 助手。',
                    'short_description': 'Anthropic Claude-3 Opus，5倍使用量',
                    'price_usd': 75.0,
                    'price_unit': '月',
                    'image_url': 'assets/images/claudemax.jpg',
                    'page_url': 'pages/claude.html',
                    'in_stock': True,
                    'stock_quantity': 30,
                    'is_featured': True,
                    'sort_order': 2,
                    'category': 'AI对话助手',
                    'features': json.dumps([
                        'Claude-3 Opus 模型',
                        '5倍标准使用量',
                        '长文本处理能力',
                        '高级推理能力'
                    ]),
                    'seo_title': '购买 Claude Max 5x 帐号 - Anthropic 官方增强版',
                    'seo_description': '购买 Claude Max 5x 帐号，享受 5 倍使用量的 Claude-3 Opus。安全 USDT 支付。',
                    'seo_keywords': 'Claude Max, Claude-3 Opus, Anthropic, AI助手, USDT支付'
                },
                {
                    'name': 'Super Grok',
                    'slug': 'super-grok',
                    'description': '体验 xAI 的 Super Grok，X 平台专属的实时 AI 助手。',
                    'short_description': 'xAI 出品，X 平台深度整合',
                    'price_usd': 20.0,
                    'price_unit': '月',
                    'image_url': 'assets/images/grokpro.jpeg',
                    'page_url': 'pages/grok.html',
                    'in_stock': True,
                    'stock_quantity': 100,
                    'is_featured': False,
                    'sort_order': 3,
                    'category': 'AI对话助手',
                    'features': json.dumps([
                        'X 平台实时信息',
                        '独特幽默个性',
                        'Grok-1 模型支持',
                        '处理敏感话题'
                    ]),
                    'seo_title': '购买 Super Grok 帐号 - X平台实时AI助手',
                    'seo_description': '购买 Super Grok 帐号，体验 xAI 的实时 AI 助手。集成 X 平台信息。',
                    'seo_keywords': 'Super Grok, xAI, X平台, 实时AI, Grok-1, USDT支付'
                },
                {
                    'name': 'Cursor Pro',
                    'slug': 'cursor-pro',
                    'description': '体验 Cursor Pro，AI 协同编程的未来。',
                    'short_description': 'AI-First Code Editor，GPT-4 Turbo 驱动',
                    'price_usd': 12.0,
                    'price_unit': '月',
                    'image_url': 'assets/images/curserpro.jpg',
                    'page_url': 'pages/cursor.html',
                    'in_stock': True,
                    'stock_quantity': 200,
                    'is_featured': False,
                    'sort_order': 4,
                    'category': 'AI开发工具',
                    'features': json.dumps([
                        'GPT-4 Turbo 无限制',
                        'AI 代码生成',
                        '智能代码重构',
                        '多语言支持'
                    ]),
                    'seo_title': '购买 Cursor Pro 帐号 - AI 协同智能开发环境',
                    'seo_description': '购买 Cursor Pro 帐号，体验 AI 驱动的智能编程环境。GPT-4 Turbo 支持。',
                    'seo_keywords': 'Cursor Pro, AI编程, GPT-4 Turbo, 代码生成, IDE, USDT支付'
                },
                {
                    'name': 'Lovable Pro 200 Credit',
                    'slug': 'lovable-pro-200-credit',
                    'description': '体验 Lovable Pro，AI 驱动的全栈应用开发平台。',
                    'short_description': 'AI 全栈应用开发平台，快速原型与部署',
                    'price_usd': 35.0,
                    'price_unit': '200 Credit',
                    'image_url': 'assets/images/lovable.png',
                    'page_url': 'pages/lovable.html',
                    'in_stock': True,
                    'stock_quantity': 80,
                    'is_featured': False,
                    'sort_order': 5,
                    'category': 'AI开发工具',
                    'features': json.dumps([
                        'AI 全栈开发',
                        '200 Credit 额度',
                        '快速原型验证',
                        '多技术栈支持'
                    ]),
                    'seo_title': '购买 Lovable Pro 200 Credit - AI驱动全栈应用开发',
                    'seo_description': '购买 Lovable Pro 200 Credit，体验 AI 驱动的全栈应用开发。快速原型到部署。',
                    'seo_keywords': 'Lovable Pro, AI全栈开发, 200 Credit, 快速原型, USDT支付'
                }
            ]
            
            for product_data in default_products:
                product = Product(**product_data)
                db.session.add(product)
            
            db.session.commit()
            print("Initialized database with default products.")
        
        print("Database initialization completed.")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)  # URL友好的标识符，如 'chatgpt-pro'
    description = db.Column(db.Text)
    short_description = db.Column(db.String(200))  # 用于卡片显示的简短描述
    price_usd = db.Column(db.Float, nullable=False)
    price_unit = db.Column(db.String(20), default='月')  # 价格单位，如 '月', '200 Credit'
    image_url = db.Column(db.String(200))
    page_url = db.Column(db.String(200))  # 产品详情页面URL，如 'pages/chatgpt.html'
    
    # 库存和状态
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=999)  # -1 表示无限库存
    is_featured = db.Column(db.Boolean, default=False)  # 是否为特色产品
    is_active = db.Column(db.Boolean, default=True)  # 是否激活显示
    
    # 排序和分类
    sort_order = db.Column(db.Integer, default=0)  # 用于排序显示
    category = db.Column(db.String(50), default='AI工具')  # 产品分类
    
    # 特性列表 (JSON格式存储)
    features = db.Column(db.Text)  # JSON字符串，存储产品特性列表
    
    # SEO
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(500))
    seo_keywords = db.Column(db.String(500))
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        import json
        features_list = []
        if self.features:
            try:
                features_list = json.loads(self.features)
            except:
                features_list = []
        
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'short_description': self.short_description,
            'price_usd': self.price_usd,
            'price_unit': self.price_unit,
            'image_url': self.image_url,
            'page_url': self.page_url,
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'category': self.category,
            'features': features_list,
            'seo_title': self.seo_title,
            'seo_description': self.seo_description,
            'seo_keywords': self.seo_keywords,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)  # 订单ID
    
    # 用户信息
    customer_email = db.Column(db.String(120), nullable=False)
    
    # 产品信息
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)  # 冗余存储，防止产品删除后丢失信息
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # 价格信息
    unit_price_usd = db.Column(db.Float, nullable=False)  # 单价（USDT）
    total_amount_usd = db.Column(db.Float, nullable=False)  # 总价（USDT）
    price_unit = db.Column(db.String(20), nullable=False)  # 价格单位
    
    # 支付信息
    payment_method = db.Column(db.String(20), nullable=False)  # 'usdt' 或 'alipay'
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    
    # OxaPay相关
    oxapay_order_id = db.Column(db.String(100))  # OxaPay返回的订单ID
    oxapay_track_id = db.Column(db.String(100))  # OxaPay跟踪ID
    oxapay_pay_link = db.Column(db.String(500))  # OxaPay支付链接
    
    # 订单状态
    order_status = db.Column(db.String(20), default='created')  # created, processing, completed, cancelled
    delivery_status = db.Column(db.String(20), default='pending')  # pending, delivered, failed
    
    # 备注信息
    customer_notes = db.Column(db.Text)  # 客户备注
    admin_notes = db.Column(db.Text)  # 管理员备注
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    paid_at = db.Column(db.DateTime)  # 支付完成时间
    delivered_at = db.Column(db.DateTime)  # 交付完成时间
    
    # 关联关系
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_email': self.customer_email,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price_usd': self.unit_price_usd,
            'total_amount_usd': self.total_amount_usd,
            'price_unit': self.price_unit,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'oxapay_order_id': self.oxapay_order_id,
            'oxapay_track_id': self.oxapay_track_id,
            'oxapay_pay_link': self.oxapay_pay_link,
            'order_status': self.order_status,
            'delivery_status': self.delivery_status,
            'customer_notes': self.customer_notes,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }

class Announcement(db.Model):
    """公告模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # 公告标题
    content = db.Column(db.Text, nullable=False)  # 公告内容
    announcement_date = db.Column(db.Date, nullable=False)  # 公告日期
    is_active = db.Column(db.Boolean, default=True)  # 是否激活显示
    is_pinned = db.Column(db.Boolean, default=False)  # 是否置顶
    sort_order = db.Column(db.Integer, default=0)  # 排序权重
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'announcement_date': self.announcement_date.isoformat() if self.announcement_date else None,
            'is_active': self.is_active,
            'is_pinned': self.is_pinned,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DiscountCode(db.Model):
    """优惠代码模型"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # 优惠代码
    discount_type = db.Column(db.String(20), default='percentage')  # 'percentage' 或 'fixed'
    discount_value = db.Column(db.Float, nullable=False)  # 折扣值（百分比或固定金额）
    description = db.Column(db.String(200))  # 优惠描述
    
    # 使用限制
    max_uses = db.Column(db.Integer, default=-1)  # 最大使用次数，-1表示无限制
    used_count = db.Column(db.Integer, default=0)  # 已使用次数
    min_order_amount = db.Column(db.Float, default=0)  # 最小订单金额
    
    # 有效期
    valid_from = db.Column(db.DateTime)  # 有效开始时间
    valid_until = db.Column(db.DateTime)  # 有效结束时间
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'description': self.description,
            'max_uses': self.max_uses,
            'used_count': self.used_count,
            'min_order_amount': self.min_order_amount,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_valid(self, order_amount=0):
        """检查优惠代码是否有效"""
        from datetime import datetime, timezone
        
        if not self.is_active:
            return False, "优惠代码已禁用"
        
        # 检查使用次数
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False, "优惠代码使用次数已达上限"
        
        # 检查最小订单金额
        if order_amount < self.min_order_amount:
            return False, f"订单金额需满足最低 ${self.min_order_amount} USDT"
        
        # 检查有效期
        now = datetime.now(timezone.utc)
        if self.valid_from and now < self.valid_from:
            return False, "优惠代码尚未生效"
        
        if self.valid_until and now > self.valid_until:
            return False, "优惠代码已过期"
        
        return True, "优惠代码有效"
    
    def calculate_discount(self, order_amount):
        """计算折扣金额"""
        if self.discount_type == 'percentage':
            # 百分比折扣
            discount_amount = order_amount * (self.discount_value / 100)
        else:
            # 固定金额折扣
            discount_amount = min(self.discount_value, order_amount)
        
        return round(discount_amount, 2) 