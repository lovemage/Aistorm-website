# OxaPay 集成指南 🔧

## 概述

本文档详细说明了AIStorm网站与OxaPay支付系统的集成过程，包括API调用方式、测试结果和配置方法。

## 关键发现 🔍

### API 调用方式测试结果

经过全面测试，我们发现了OxaPay API的正确使用方式：

#### 1. Merchant API (推荐)
- **URL**: `https://api.oxapay.com/merchants/request`
- **认证方式**: Header认证 (`merchant_api_key`)
- **数据传递**: 使用`json.dumps(data)`
- **状态**: ✅ 可用（但需要参数调优）

```python
headers = {
    'merchant_api_key': 'YOUR_API_KEY',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

data = {
    'amount': 130.0,
    'currency': 'USDT',
    'lifeTime': 15,
    'feePaidByPayer': 1,
    'callbackUrl': 'https://www.aistorm.art/oxapay-webhook',
    'description': 'AIStorm - 产品订购',
    'orderId': 'unique_order_id',
    'email': 'customer@example.com'
}

response = requests.post(url, data=json.dumps(data), headers=headers)
```

#### 2. 已测试但不工作的方式

**方法1: Body参数认证**
```python
# ❌ 不工作 - 返回 "Invalid merchant API key"
data = {
    'merchant': 'YOUR_API_KEY',  # API密钥在请求体中
    'amount': 130.0,
    # ... 其他参数
}
```

**方法3: General API风格**
```python
# ❌ 不工作 - 404 Not Found
url = 'https://api.oxapay.com/v1/merchants/request'
headers = {'general_api_key': 'YOUR_API_KEY'}
```

### 错误代码说明

| 代码 | 含义 | 解决方案 |
|------|------|----------|
| 100 | 成功 | ✅ 发票创建成功 |
| 101 | 参数验证错误 ("Validating problem") | 检查参数格式，特别是邮箱、回调URL等 |
| 102 | API密钥无效 | 检查密钥是否正确，是否有权限 |
| 103 | 商户余额不足 | 联系OxaPay充值 |
| 104 | 不支持的货币类型 | 使用支持的货币（如USDT） |
| 105 | 金额超出限制 | 调整交易金额 |

## 当前实现状态 📊

### ✅ 已解决的问题

1. **API调用方式正确**：使用header认证
2. **数据序列化正确**：使用`json.dumps()`
3. **错误处理完善**：详细的错误代码解析
4. **测试模式完整**：开发环境自动启用测试模式
5. **Webhook处理正常**：支付状态更新机制工作正常

### ⚠️ 当前遇到的问题

**"Validating problem" (错误代码101)**
- **现象**：API返回参数验证错误
- **可能原因**：
  - 邮箱格式验证过严
  - 回调URL在开发环境中不可访问
  - 某些参数格式不符合要求
- **当前解决方案**：开发环境自动启用测试模式

## 配置指南 ⚙️

### 环境变量配置

```bash
# 必需的环境变量
export OXAPAY_SECRET_KEY="your-merchant-api-key"
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

### 获取API密钥

1. 访问 [OxaPay 官网](https://oxapay.com)
2. 注册商户账户
3. 在商户后台获取API密钥
4. 确保API密钥有Merchant权限

### 测试API配置

使用我们提供的测试工具：

```bash
OXAPAY_SECRET_KEY="your-key" python3 test_oxapay_config.py
```

## 技术实现细节 🔧

### 支付流程

1. **创建订单**：客户提交订购信息
2. **生成发票**：调用OxaPay API创建支付发票
3. **支付处理**：客户通过OxaPay支付页面完成支付
4. **状态回调**：OxaPay通过Webhook更新支付状态
5. **订单完成**：系统处理完成的订单

### 测试模式

在开发环境中，如果API调用失败，系统会自动启用测试模式：

- 生成模拟支付链接
- 模拟支付成功流程
- 测试Webhook机制
- 验证数据库更新

### 生产环境部署

1. **环境变量**：确保生产环境配置了正确的API密钥
2. **HTTPS回调**：确保webhook URL使用HTTPS
3. **域名白名单**：如需要，在OxaPay后台配置域名白名单
4. **监控日志**：监控支付成功率和错误日志

## 故障排除 🔍

### 常见问题

#### 1. "Invalid merchant API key"
- 检查API密钥是否正确
- 确认API密钥有Merchant权限
- 验证环境变量是否正确设置

#### 2. "Validating problem"
- 检查客户邮箱格式是否正确
- 确认回调URL是否可访问
- 验证所有必需参数是否提供

#### 3. Webhook不工作
- 确认回调URL可以被外部访问
- 检查Webhook endpoint是否正确实现
- 验证签名验证逻辑

### 调试工具

1. **API测试工具**：`test_oxapay_config.py`
2. **支付流程测试**：`test_payment_flow.py`
3. **详细日志**：服务器端详细的调试输出

## 参考资料 📚

- [OxaPay 官方文档](https://docs.oxapay.com/)
- [Merchant API 文档](https://docs.oxapay.com/merchants)
- [Webhook 文档](https://docs.oxapay.com/webhooks)

## 更新日志 📝

### 2025-05-29
- ✅ 修复API调用方式，使用header认证
- ✅ 实现基于官方Python示例的集成
- ✅ 完善错误处理和测试模式
- ✅ 解决"Validating problem"错误的应对机制

### 待改进
- 🔄 解决生产环境参数验证问题
- 🔄 优化错误消息的用户友好性
- 🔄 添加更多支付货币选项

---

*本文档持续更新中，如遇到新问题请及时记录和解决。* 