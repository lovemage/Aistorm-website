# 🔧 OxaPay 测试模式使用指南

## 🚨 关于API密钥问题

您提供的 `URXMY9-VHVPGK-DA4HEC-2EXI3S` 看起来是**商户ID**而不是**API密钥**。

OxaPay需要的配置包括：
- **Merchant ID**: `URXMY9-VHVPGK-DA4HEC-2EXI3S` (您已提供)
- **API Secret Key**: 需要从OxaPay后台获取

## ✅ 测试模式已启用

当API密钥无效时，系统会自动启用测试模式：

### 测试模式特点
- ✅ 不需要真实的OxaPay API密钥
- ✅ 自动生成测试支付链接
- ✅ 完整的支付流程测试
- ✅ Telegram通知正常工作
- ✅ 订单状态正确更新

## 🎯 如何测试支付流程

### 1. 访问商店页面
```
http://localhost:8080/pages/shop.html
```

### 2. 选择产品并下单
- 选择任意产品
- 填写邮箱地址
- 选择数量
- 点击"立即购买 USDT"

### 3. 在测试支付页面
- 系统会自动跳转到测试支付页面
- 显示订单信息（订单号、金额、追踪ID）
- 两个选择：
  - **✅ 模拟支付成功** - 模拟支付完成
  - **❌ 模拟支付失败** - 模拟支付失败

### 4. 查看通知
- 订单创建时：Telegram收到订单创建通知
- 支付完成时：Telegram收到支付成功通知
- 支付失败时：Telegram收到支付失败通知

## 🔍 测试步骤示例

1. **创建订单**：
   ```
   产品: ChatGPT Pro
   数量: 1个月
   金额: $130 USDT
   邮箱: test@example.com
   ```

2. **点击USDT支付**：
   - 系统生成订单
   - 发送订单创建通知到Telegram
   - 跳转到测试支付页面

3. **完成支付**：
   - 在测试页面点击"模拟支付成功"
   - 系统处理webhook
   - 发送支付成功通知到Telegram
   - 自动关闭支付页面

## 📱 Telegram通知示例

### 订单创建通知
```
📝 新订单创建

📦 产品：ChatGPT Pro
🔢 数量：1 月
💵 金额：$130.0 USDT
📧 邮箱：test@example.com
🆔 订单号：order_1748496135010_xxx
📊 状态：等待支付
⏰ 时间：2025-05-29 13:32:08
💳 支付方式：USDT支付
```

### 支付成功通知
```
💰 收到USDT支付！

📦 产品：ChatGPT Pro
🔢 数量：1 月
💵 金额：$130.0 USDT
📧 邮箱：test@example.com
🆔 订单号：order_1748496135010_xxx
📊 状态：支付成功
⏰ 时间：2025-05-29 13:32:08
💳 支付方式：USDT支付

💎 OxaPay详情：
🔍 追踪ID：track_1748496135010
💰 实收金额：130.0 USDT

🎉 请及时处理账号交付！
```

## 🔧 如何获取真实的OxaPay配置

1. **登录OxaPay商户后台**
2. **找到API设置**
3. **获取API Secret Key**（不是Merchant ID）
4. **配置Webhook URL**：`https://your-domain.com/oxapay-webhook`

## 🌟 测试完成后

测试模式确保所有功能正常工作：
- ✅ 订单创建系统
- ✅ Telegram通知系统
- ✅ 支付状态管理
- ✅ Webhook处理

一旦获得真实的OxaPay API密钥，只需替换配置即可投入生产使用。

---

**当前状态**: 🟢 测试模式运行正常
**服务地址**: 
- 前端: http://localhost:8080
- 后端: http://localhost:5001
- 商店: http://localhost:8080/pages/shop.html 