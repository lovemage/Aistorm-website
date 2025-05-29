# AIStorm 生产模式配置指南

## 🎯 **从测试模式切换到正常模式**

系统现在支持通过环境变量控制支付模式：

### 📋 **支付模式说明**

#### 🧪 **测试模式** (默认关闭)
- 自动处理OxaPay API错误
- 提供模拟支付流程
- 适用于开发和演示

#### 🏭 **正常模式** (默认开启)
- 直接使用OxaPay真实支付
- 错误时返回具体错误信息
- 适用于生产环境

## 🔧 **环境变量配置**

### Railway部署配置

在Railway的Variables标签页中设置：

#### 基本配置（必需）
```bash
TELEGRAM_BOT_TOKEN = 7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA
TELEGRAM_CHAT_ID = 7935635650
OXAPAY_SECRET_KEY = URXMY9-VHVPGK-DA4HEC-2EXI3S
FLASK_ENV = production
PORT = 5000
```

#### 支付模式控制（可选）
```bash
# 正常模式（默认，推荐生产环境）
FORCE_TEST_MODE = false

# 或者强制测试模式（如果需要）
FORCE_TEST_MODE = true
```

## 🔄 **模式切换步骤**

### 切换到正常模式（推荐）

1. **在Railway中删除或设置**：
   ```bash
   FORCE_TEST_MODE = false
   ```
   或者完全不设置这个变量（默认就是正常模式）

2. **重新部署**：
   - Railway会自动检测环境变量变化
   - 自动重新部署应用

3. **验证配置**：
   - 支付时将使用真实的OxaPay API
   - 如果遇到API错误，会显示具体错误信息

### 切换到测试模式（如果需要）

1. **在Railway中设置**：
   ```bash
   FORCE_TEST_MODE = true
   ```

2. **重新部署并验证**

## 🧪 **测试验证**

### 正常模式验证

1. **创建订单**：
   - 访问商店页面
   - 选择产品并生成订单

2. **预期行为**：
   - 如果OxaPay配置正确：生成真实支付链接
   - 如果OxaPay有问题：显示具体错误信息

3. **错误示例**：
   ```json
   {
     "success": false,
     "error": "支付参数验证失败: Validating problem",
     "details": "请检查订单金额、邮箱格式、或联系客服"
   }
   ```

### 测试模式验证

1. **强制测试模式启用后**：
   - 支付始终进入测试模式
   - 显示测试支付页面

2. **测试响应示例**：
   ```json
   {
     "success": true,
     "testMode": true,
     "message": "强制测试模式 - 参数验证失败",
     "payLink": "https://your-domain.railway.app/test_payment_success.html?..."
   }
   ```

## 🔍 **故障排除**

### 常见OxaPay错误

#### 错误101：参数验证失败
**可能原因**：
- 邮箱格式不正确
- 金额超出限制
- 回调URL无法访问
- 货币类型不支持

**解决方案**：
1. 检查订单数据格式
2. 验证回调URL可访问性
3. 联系OxaPay客服确认账户状态

#### 错误102：API密钥无效
**可能原因**：
- API密钥错误或过期
- 账户被暂停
- 权限不足

**解决方案**：
1. 验证API密钥正确性
2. 联系OxaPay客服检查账户状态
3. 申请新的API密钥

### 调试步骤

1. **查看Railway日志**：
   ```bash
   # 在Railway Dashboard中查看Logs
   ```

2. **检查API请求**：
   - 查看发送到OxaPay的具体参数
   - 验证响应内容

3. **测试API密钥**：
   - 可以暂时启用测试模式验证系统功能
   - 联系OxaPay技术支持

## 📊 **生产环境建议**

### 推荐配置

```bash
# 生产环境推荐配置
TELEGRAM_BOT_TOKEN = 7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA
TELEGRAM_CHAT_ID = 7935635650
OXAPAY_SECRET_KEY = URXMY9-VHVPGK-DA4HEC-2EXI3S
FLASK_ENV = production
PORT = 5000
# FORCE_TEST_MODE 不设置或设置为 false（正常模式）
```

### 监控要点

1. **支付成功率**：监控支付API调用成功率
2. **错误日志**：关注101/102错误频率
3. **用户反馈**：收集支付流程用户体验反馈
4. **Telegram通知**：确保订单通知正常发送

## ✅ **配置完成检查清单**

- [ ] 环境变量正确设置
- [ ] FORCE_TEST_MODE 设置为 false 或不设置
- [ ] Railway重新部署成功
- [ ] 测试支付流程（真实模式）
- [ ] 验证错误处理正常
- [ ] Telegram通知正常工作

---

**当前推荐配置**: 正常模式（FORCE_TEST_MODE=false）
**适用场景**: 生产环境，真实支付处理
**回退方案**: 如遇问题可临时启用测试模式 