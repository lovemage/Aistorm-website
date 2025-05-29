# AIStorm 远程测试部署指南

## 🎯 **部署目标**

将AIStorm支付系统部署到远程环境进行完整测试，确保所有功能在生产环境中正常工作。

## 📋 **当前系统状态**

### ✅ **本地测试完成**
- 支付系统：完全正常（测试模式）
- API密钥：正确配置并通过验证
- Telegram通知：正常工作
- 数据库：正常连接和操作
- 用户体验：友好的错误提示和测试模式

### 📊 **测试数据**
```bash
# 最新测试结果（本地）
✅ API密钥检查通过: URXMY9-V...
✅ 订单创建成功
✅ 支付链接生成（测试模式）
✅ Telegram通知发送成功
✅ Webhook处理正常
```

## 🚀 **部署方案选择**

### 方案1：Railway部署（推荐）
**优势**：
- 自动部署，支持Git集成
- 免费额度充足
- 支持环境变量配置
- 自动HTTPS

**部署步骤**：
1. 访问 https://railway.app
2. 连接GitHub仓库
3. 配置环境变量
4. 自动部署

### 方案2：Vercel部署
**优势**：
- 静态文件托管优秀
- 免费部署
- 全球CDN

**注意**：需要配置Serverless Functions

### 方案3：Heroku部署
**优势**：
- 成熟稳定
- 支持多种语言
- 丰富的插件生态

## 🔧 **环境变量配置**

无论选择哪种部署方案，都需要配置以下环境变量：

```bash
# 必需环境变量
TELEGRAM_BOT_TOKEN=7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA
TELEGRAM_CHAT_ID=7935635650
OXAPAY_SECRET_KEY=URXMY9-VHVPGK-DA4HEC-2EXI3S

# 可选环境变量
FLASK_ENV=production
SECRET_KEY=your-secret-key-for-production
PORT=5000
```

## 📝 **Railway快速部署**

### 1. 创建Railway项目

```bash
# 方法1：通过Web界面
1. 访问 https://railway.app
2. 点击 "Start a New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择您的仓库：lovemage/Aistorm-website

# 方法2：通过CLI
npm install -g @railway/cli
railway login
railway init
railway link [project-id]
```

### 2. 配置环境变量

在Railway Dashboard中设置：

```bash
TELEGRAM_BOT_TOKEN → 7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA
TELEGRAM_CHAT_ID → 7935635650
OXAPAY_SECRET_KEY → URXMY9-VHVPGK-DA4HEC-2EXI3S
FLASK_ENV → production
PORT → 5000
```

### 3. 创建部署配置文件

确保根目录有以下文件：

**Procfile**:
```
web: python backend/app.py
```

**runtime.txt**:
```
python-3.11.0
```

**requirements.txt**:
```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
requests==2.31.0
python-dotenv==1.0.0
```

## 🧪 **测试计划**

### 阶段1：基础功能测试
- [ ] 网站首页加载
- [ ] 产品列表API
- [ ] 静态资源加载

### 阶段2：支付系统测试
- [ ] 订单创建
- [ ] 支付链接生成
- [ ] 测试模式验证

### 阶段3：通知系统测试
- [ ] Telegram通知发送
- [ ] 订单状态更新
- [ ] Webhook处理

### 阶段4：完整流程测试
- [ ] 端到端支付流程
- [ ] 错误处理验证
- [ ] 用户体验测试

## 📊 **监控和调试**

### 1. 日志查看

**Railway**:
```bash
railway logs
```

**Vercel**:
```bash
vercel logs [deployment-url]
```

### 2. 环境变量验证

**测试端点**:
```bash
curl https://your-domain.com/api/test-telegram
```

### 3. 健康检查

**API状态**:
```bash
curl https://your-domain.com/api/products
curl https://your-domain.com/api/settings
```

## 🔍 **常见问题解决**

### 问题1：环境变量未生效
**解决方案**：
1. 检查变量名拼写
2. 重新部署应用
3. 查看部署日志

### 问题2：静态文件404
**解决方案**：
1. 检查文件路径
2. 配置静态文件服务
3. 验证CORS设置

### 问题3：数据库连接失败
**解决方案**：
1. 使用SQLite（无需额外配置）
2. 检查数据库文件权限
3. 验证连接字符串

## 🎯 **部署检查清单**

### 部署前：
- [ ] 代码已提交到Git
- [ ] 环境变量已准备
- [ ] 部署配置文件已创建
- [ ] 本地测试通过

### 部署后：
- [ ] 应用启动成功
- [ ] 环境变量生效
- [ ] API响应正常
- [ ] 支付流程工作
- [ ] Telegram通知正常

## 🚀 **开始部署**

**推荐步骤**：

1. **选择Railway部署**（最简单）
2. **配置环境变量**
3. **验证基础功能**
4. **测试支付流程**
5. **确认生产就绪**

## 📞 **技术支持**

如果在部署过程中遇到问题：

1. **查看部署日志**
2. **检查环境变量配置**
3. **验证API密钥**
4. **测试网络连接**

---

**当前状态**: ✅ 代码已推送，准备远程部署
**推荐方案**: Railway部署（支持Python，配置简单）
**预计时间**: 10-15分钟 