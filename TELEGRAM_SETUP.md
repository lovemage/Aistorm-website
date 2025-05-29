# AIStorm Telegram Bot 设置指南

## 📱 Telegram Bot 配置步骤

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/start` 开始与 BotFather 对话
3. 发送 `/newbot` 创建新机器人
4. 按提示设置机器人名称和用户名
5. 获取 Bot Token (格式类似: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. 获取 Chat ID

**方法一：使用 @userinfobot**
1. 在 Telegram 中搜索 `@userinfobot`
2. 发送 `/start` 获取您的用户 ID

**方法二：使用您的 Bot**
1. 先向您的 Bot 发送任意消息
2. 访问: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. 在返回的 JSON 中查找 `chat.id`

### 3. 配置环境变量

创建 `.env` 文件（或设置系统环境变量）：

```bash
# Telegram Bot Token (从 @BotFather 获取)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Chat ID (您的用户ID或群组ID)
TELEGRAM_CHAT_ID=123456789

# OxaPay 密钥 (用于验证webhook签名)
OXAPAY_SECRET_KEY=your-oxapay-secret-key
```

### 4. 测试配置

#### 使用测试页面
1. 访问: `http://localhost:8000/test_payment.html`
2. 点击 "5. 查看Telegram配置" 检查配置状态
3. 点击 "4. 测试Telegram通知" 发送测试消息

#### 使用API直接测试
```bash
# 测试配置状态
curl -X POST "http://localhost:5001/api/test-telegram" \
  -H "Content-Type: application/json" \
  -d '{"type": "config"}'

# 发送测试消息
curl -X POST "http://localhost:5001/api/test-telegram" \
  -H "Content-Type: application/json" \
  -d '{"type": "test"}'
```

## 🔔 通知功能说明

### 自动通知事件

1. **订单创建** - 用户创建新订单时
2. **支付成功** - 收到OxaPay支付确认时
3. **支付失败** - 支付失败或过期时
4. **状态更新** - 订单状态变化时

### 通知消息格式

**订单创建通知：**
```
📝 新订单创建

📦 产品：ChatGPT Pro
🔢 数量：1 月
💵 金额：$130 USDT
📧 邮箱：user@example.com
🆔 订单号：order_1234567890
📊 状态：等待支付
⏰ 时间：2025-05-29 13:19:47

💳 支付方式：USDT支付
```

**支付成功通知：**
```
💰 收到USDT支付！

📦 产品：ChatGPT Pro
🔢 数量：1 月
💵 金额：$130 USDT
📧 邮箱：user@example.com
🆔 订单号：order_1234567890
📊 状态：支付成功
⏰ 时间：2025-05-29 13:19:47

💳 支付方式：USDT支付

💎 OxaPay详情：
🔍 追踪ID: track_1234567890
💰 实收金额: 130 USDT

🎉 请及时处理账号交付！
```

## 🔒 安全配置

### Webhook 签名验证

如果配置了 `OXAPAY_SECRET_KEY`，系统会验证来自 OxaPay 的 webhook 签名：

```python
# 签名验证逻辑
sign_string = f"{order_id}{OXAPAY_SECRET_KEY}"
calculated_sign = hashlib.sha256(sign_string.encode()).hexdigest()
```

### 环境变量安全

- 永远不要将真实的 Token 和密钥提交到代码仓库
- 在生产环境中使用强密钥
- 定期轮换 Bot Token

## 🚀 部署注意事项

### Railway 部署

在 Railway 中设置环境变量：
1. 进入项目设置
2. 点击 Variables 标签
3. 添加所需的环境变量

### Heroku 部署

```bash
heroku config:set TELEGRAM_BOT_TOKEN=your-token
heroku config:set TELEGRAM_CHAT_ID=your-chat-id
heroku config:set OXAPAY_SECRET_KEY=your-secret
```

### 本地开发

创建 `.env` 文件（已在 .gitignore 中忽略）：
```bash
cp env_example.txt .env
# 编辑 .env 文件，填入真实值
```

## 📞 故障排除

### 常见问题

1. **Bot Token 无效**
   - 检查从 @BotFather 获取的 Token 是否正确
   - 确保 Token 没有过期

2. **Chat ID 无效**
   - 确保已向 Bot 发送过消息
   - 检查 Chat ID 格式是否正确

3. **消息发送失败**
   - 检查 Bot 是否被阻止
   - 确认网络连接正常

4. **环境变量未生效**
   - 重启应用服务器
   - 检查环境变量名称是否正确

### 日志信息

启动时会显示配置状态：
- `✅ Telegram Bot 初始化成功` - 配置正确
- `ℹ️ Telegram Bot 配置不完整` - 缺少配置
- `❌ Telegram Bot 初始化失败` - Token 无效

## 🔄 后续扩展

可以进一步扩展的功能：
- 群组通知支持
- 订单管理命令
- 支付状态查询
- 自动回复功能
- 多语言支持

---

如有问题，请检查后端日志或使用测试 API 进行诊断。 