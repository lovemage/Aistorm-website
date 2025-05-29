# AIStorm 静态网站 + 后台管理系统

> 一个完整的AI产品销售网站，包含现代化前端和功能完整的后台管理系统

## 🌟 核心特性

- **🎨 现代化前端**: 响应式设计，AI产品展示
- **🔐 后台管理**: 产品管理、订单系统、数据统计
- **💰 支付集成**: OxaPay USDT支付，Telegram通知
- **🚀 云端部署**: 支持Railway、Render等平台一键部署

## 🚀 快速开始

### 本地运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量（复制并编辑）
cp .env.example .env

# 3. 启动应用
python3 start.py
```

### 云端部署
```bash
# Railway一键部署
git push origin main
# 在Railway中连接GitHub仓库并部署
```

## 🔑 默认登录

- **前端**: http://localhost:5001/
- **后台**: http://localhost:5001/admin
- **用户名**: admin
- **密码**: admin123

⚠️ **重要**: 首次登录后请立即修改默认密码！

## 📁 项目结构

```
AIStorm_Static_Website/
├── 📄 index.html              # 前端主页
├── 📁 pages/                  # 产品详情页面
├── 📁 assets/                 # 静态资源
├── 📁 backend/                # 后台系统核心
├── 📁 templates/admin/        # 管理页面模板
├── 📁 docs/                   # 📚 完整文档
│   ├── deployment/            # 部署指南
│   ├── development/           # 开发指南
│   └── guides/               # 技术指南
├── 📄 start.py               # 启动脚本
├── 📄 requirements.txt       # Python依赖
└── 📄 railway.json          # 部署配置
```

## 📚 详细文档

### 部署相关
- **[部署指南](docs/deployment/README.md)** - 完整的部署教程和问题解决
- **[Railway部署修复](docs/deployment/RAILWAY_DEPLOYMENT_FIXED.md)** - 最新修复报告

### 开发相关  
- **[开发指南](docs/development/README.md)** - 前端开发、主题系统、API集成
- **[技术指南](docs/guides/TECHNICAL_GUIDE.md)** - Telegram、支付、安全配置

### 配置指南
- **[项目概览](docs/PROJECT_OVERVIEW.md)** - 项目架构和功能介绍
- **[更新日志](docs/CHANGELOG.md)** - 版本更新记录

## 🔧 环境变量配置

在生产环境中需要设置以下环境变量：
```bash
TELEGRAM_BOT_TOKEN=你的-telegram-bot-token
TELEGRAM_CHAT_ID=你的-telegram-chat-id  
OXAPAY_SECRET_KEY=你的-oxapay-api-key
SECRET_KEY=你的-flask-密钥
FLASK_ENV=production
```

## 🛠️ 技术栈

**后端**: Python Flask, SQLAlchemy, SQLite  
**前端**: HTML5, CSS3, JavaScript  
**支付**: OxaPay USDT  
**通知**: Telegram Bot API  
**部署**: Railway, Render, Heroku

## 📦 功能模块

- ✅ 用户身份验证和会话管理
- ✅ 产品管理（CRUD、库存、价格）
- ✅ 订单系统和支付处理
- ✅ Telegram实时通知
- ✅ 站点配置管理
- ✅ 响应式前端设计
- ✅ RESTful API接口

## 🐛 问题排除

遇到问题？请查看：
1. **[技术指南](docs/guides/TECHNICAL_GUIDE.md#故障排除)** - 常见问题解决
2. **[部署指南](docs/deployment/README.md#故障排除)** - 部署问题修复
3. **项目日志** - 检查应用运行日志

## 📞 技术支持

- 📖 查看 [完整文档](docs/README.md)
- 🔧 阅读 [技术指南](docs/guides/TECHNICAL_GUIDE.md)
- 🚀 参考 [部署指南](docs/deployment/README.md)
- 💻 浏览 [开发指南](docs/development/README.md)

## 📄 许可证

© 2025 AIStorm. 保留所有权利.

---

**AIStorm** - 让AI产品销售变得简单高效！ 🚀 