# 🔧 AIStorm 技术指南

## 📋 目录
- [Telegram Bot配置](#telegram-bot配置)
- [支付系统集成](#支付系统集成)
- [安全配置](#安全配置)
- [OxaPay测试](#oxapay测试)
- [故障排除](#故障排除)

---

## 🤖 Telegram Bot配置

### 创建Bot
1. **联系 @BotFather**
   - 在Telegram中搜索 @BotFather
   - 发送 `/newbot` 命令
   - 按提示设置Bot名称和用户名

2. **获取Bot Token**
   ```
   格式: 123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   示例: 7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA
   ```

3. **获取Chat ID**
   ```bash
   # 方法1: 通过Bot发送消息后查看
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   
   # 方法2: 使用 @userinfobot
   # 在Telegram中搜索 @userinfobot，发送任意消息获取您的用户ID
   ```

### 环境变量配置
```bash
# .env 文件
TELEGRAM_BOT_TOKEN=你的-bot-token
TELEGRAM_CHAT_ID=你的-chat-id
```

### 测试Bot配置
```python
import requests

def test_telegram_bot():
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    message = "🤖 Bot测试消息"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
```

### 消息格式化
```python
def format_order_notification(order, status_type="payment"):
    """格式化订单通知消息"""
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
    
    message = f"""
{emoji} <b>{title}</b>

📦 <b>产品：</b>{order.product_name}
🔢 <b>数量：</b>{order.quantity} {order.price_unit}
💵 <b>金额：</b>${order.total_amount_usd} USDT
📧 <b>邮箱：</b>{order.customer_email}
🆔 <b>订单号：</b><code>{order.order_id}</code>
📊 <b>状态：</b>{status_text}
⏰ <b>时间：</b>{order.created_at.strftime('%Y-%m-%d %H:%M:%S')}

💳 <b>支付方式：</b>{'USDT支付' if order.payment_method == 'usdt' else '支付宝'}
"""
    
    if order.oxapay_track_id:
        message += f"🔍 <b>追踪ID：</b><code>{order.oxapay_track_id}</code>\n"
    
    return message.strip()
```

---

## 💰 支付系统集成

### OxaPay集成流程

#### 1. 创建支付请求
```python
def create_oxapay_payment(order):
    OXAPAY_API_URL = "https://api.oxapay.com/merchants/request"
    
    payload = {
        'merchant': OXAPAY_SECRET_KEY,
        'amount': float(order.total_amount_usd),
        'currency': 'USDT',
        'lifeTime': 15,  # 15分钟过期
        'feePaidByPayer': 1,
        'callbackUrl': f"{request.host_url}oxapay-webhook",
        'description': f"购买 {order.product_name} x{order.quantity}",
        'orderId': order.order_id,
        'email': order.customer_email,
    }
    
    response = requests.post(OXAPAY_API_URL, json=payload, timeout=30)
    return response.json()
```

#### 2. 处理Webhook回调
```python
@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    try:
        data = request.json
        order_id = data.get('orderId')
        status = data.get('status')
        
        # 验证签名（生产环境必须）
        if OXAPAY_SECRET_KEY and data.get('sign'):
            received_sign = data.get('sign', '')
            sign_string = f"{order_id}{OXAPAY_SECRET_KEY}"
            calculated_sign = hashlib.sha256(sign_string.encode()).hexdigest()
            
            if received_sign != calculated_sign:
                return jsonify({'error': 'Invalid signature'}), 401
        
        # 更新订单状态
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if status == 'Paid':
            order.payment_status = 'completed'
            order.order_status = 'completed'
            order.paid_at = datetime.now(timezone.utc)
            
            # 发送成功通知
            send_telegram_notification(
                format_order_notification(order, "payment")
            )
        
        db.session.commit()
        return jsonify({'success': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 支付状态管理
```python
class PaymentStatus:
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class OrderStatus:
    CREATED = 'created'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    DELIVERED = 'delivered'
```

---

## 🔒 安全配置

### 环境变量管理
```bash
# 生产环境必需的安全配置
SECRET_KEY=your-super-secret-flask-key-min-32-chars
FLASK_ENV=production
DEBUG=false

# API密钥配置
TELEGRAM_BOT_TOKEN=bot123456:your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
OXAPAY_SECRET_KEY=your-oxapay-secret-key

# 数据库配置
DATABASE_URL=sqlite:///aistorm.db

# CORS配置（可选）
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 密码安全
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
```

### API安全
```python
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin or not user.is_active:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
```

### 签名验证
```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """验证Webhook签名"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)
```

---

## 🧪 OxaPay测试

### 测试环境配置
```python
# 测试模式检测
def is_test_mode():
    return os.environ.get('OXAPAY_TEST_MODE') == 'true' or \
           not OXAPAY_SECRET_KEY or \
           OXAPAY_SECRET_KEY.startswith('test_')

# 模拟OxaPay响应
def create_test_payment_response(order):
    return {
        'result': 100,
        'orderId': f'test_{order.order_id}',
        'trackId': f'track_{int(time.time())}',
        'payLink': f'{request.host_url}test_payment_success.html?order={order.order_id}'
    }
```

### 测试用例
```python
def test_payment_flow():
    """测试完整支付流程"""
    # 1. 创建测试订单
    order_data = {
        'orderId': 'test_order_123',
        'amount': 100.0,
        'email': 'test@example.com',
        'productId': 'chatgpt-pro',
        'quantity': 1,
        'paymentMethod': 'usdt'
    }
    
    # 2. 创建订单
    response = client.post('/api/create-order', json=order_data)
    assert response.status_code == 200
    
    # 3. 发起支付
    payment_response = client.post('/api/oxapay-payment', json={'orderId': 'test_order_123'})
    assert payment_response.status_code == 200
    
    # 4. 模拟Webhook
    webhook_data = {
        'orderId': 'test_order_123',
        'status': 'Paid',
        'amount': '100.0',
        'currency': 'USDT'
    }
    
    webhook_response = client.post('/oxapay-webhook', json=webhook_data)
    assert webhook_response.status_code == 200
```

### Webhook测试工具
```html
<!-- 测试页面中的Webhook测试 -->
<script>
async function testWebhook(status) {
    const webhookData = {
        orderId: 'test_order_123',
        status: status,
        amount: '100.0',
        currency: 'USDT',
        trackId: 'test_track_123'
    };

    try {
        const response = await fetch('/oxapay-webhook', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(webhookData)
        });

        const result = await response.json();
        console.log('Webhook结果:', result);
    } catch (error) {
        console.error('Webhook错误:', error);
    }
}
</script>
```

---

## 🐛 故障排除

### 常见问题

#### 1. Telegram通知失败
```bash
# 检查Bot Token格式
echo $TELEGRAM_BOT_TOKEN | grep -E '^[0-9]+:[A-Za-z0-9_-]+$'

# 测试Bot连接
curl -X GET "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# 测试发送消息
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
     -H "Content-Type: application/json" \
     -d "{\"chat_id\":\"$TELEGRAM_CHAT_ID\",\"text\":\"测试消息\"}"
```

#### 2. OxaPay集成问题
```python
# 调试OxaPay请求
def debug_oxapay_request(payload):
    print(f"OxaPay请求数据: {json.dumps(payload, indent=2)}")
    
    # 检查必需字段
    required_fields = ['merchant', 'amount', 'currency', 'orderId']
    missing_fields = [field for field in required_fields if not payload.get(field)]
    
    if missing_fields:
        print(f"❌ 缺少必需字段: {missing_fields}")
        return False
    
    print("✅ 所有必需字段都存在")
    return True
```

#### 3. 数据库问题
```python
# 数据库连接测试
def test_database_connection():
    try:
        db.session.execute('SELECT 1')
        print("✅ 数据库连接正常")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

# 数据库初始化
def reset_database():
    """重置数据库（仅开发环境）"""
    if os.environ.get('FLASK_ENV') == 'development':
        db.drop_all()
        db.create_all()
        print("✅ 数据库已重置")
```

### 日志配置
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# 使用日志
logger = logging.getLogger(__name__)

def send_telegram_notification(message):
    try:
        # 发送逻辑
        logger.info(f"Telegram通知发送成功: {message[:50]}...")
    except Exception as e:
        logger.error(f"Telegram通知发送失败: {e}")
```

### 性能监控
```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.2f}s")
        return result
    return wrapper

@monitor_performance
def process_payment(order_data):
    # 支付处理逻辑
    pass
```

---

## 📞 技术支持

### 调试命令
```bash
# 检查所有环境变量
python3 -c "import os; [print(f'{k}={v}') for k,v in os.environ.items() if k.startswith(('TELEGRAM_', 'OXAPAY_', 'FLASK_', 'SECRET_'))]"

# 测试依赖
python3 test_dependencies.py

# 验证配置
python3 -c "from backend.app import app; print('✅ App配置正常')"
```

### 有用的资源
- [Telegram Bot API文档](https://core.telegram.org/bots/api)
- [OxaPay API文档](https://oxapay.com/docs)
- [Flask官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy文档](https://sqlalchemy.org/)

---

**更新时间**: 2025-05-29  
**维护者**: AIStorm技术团队 