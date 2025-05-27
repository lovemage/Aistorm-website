# AIStorm 项目总览

## 🌟 项目简介

AIStorm 是一个完整的AI产品销售网站，包含现代化的静态前端和功能完整的后台管理系统。专为AI产品销售和管理而设计，支持多产品展示、在线管理和配置。

## 🏗️ 项目架构

### 前端系统
- **技术栈**: HTML5 + CSS3 + JavaScript
- **设计理念**: 响应式布局，移动端优先
- **主要功能**: 产品展示、详情页面、联系方式集成
- **特色功能**: 统一主题系统、图标库、组件化设计

### 后端系统
- **技术栈**: Python Flask + SQLite + SQLAlchemy
- **架构模式**: RESTful API + 模板渲染
- **主要功能**: 用户认证、产品管理、站点配置
- **安全特性**: 密码哈希、会话管理、权限验证

## 🚀 核心功能

### 🎨 前端网站
- ✅ 现代化响应式设计
- ✅ AI产品展示页面
- ✅ 多产品详情页面
- ✅ 统一主题和图标系统
- ✅ 联系方式集成
- ✅ 价格显示（USDT + CNY估算）

### 🔧 后台管理
- ✅ 用户身份验证（用户名/密码）
- ✅ 主题配置管理（4种预设主题 + 自定义）
- ✅ 产品管理（CRUD操作、库存管理）
- ✅ 站点配置（Logo、联系方式、SEO）
- ✅ 数据统计面板
- ✅ 密码修改功能

## 📁 项目结构

```
AIStorm_Static_Website/
├── 📄 index.html                    # 前端主页
├── 📁 pages/                        # 产品详情页面
│   ├── chatgpt.html                 # ChatGPT Pro详情
│   ├── claude.html                  # Claude Max详情
│   ├── grok.html                    # Super Grok详情
│   ├── cursor.html                  # Cursor Pro详情
│   ├── lovable.html                 # Lovable Pro详情
│   └── ...                          # 其他页面
├── 📁 assets/                       # 静态资源
│   ├── css/                         # 样式文件
│   │   ├── theme-variables.css      # 主题变量系统
│   │   ├── icons.css                # 图标系统
│   │   └── mobile-nav.css           # 移动端导航
│   ├── images/                      # 图片资源
│   └── js/                          # JavaScript文件
│       ├── header.js                # 头部统一管理
│       ├── footer.js                # 页脚统一管理
│       ├── products.js              # 产品库存管理
│       └── theme-manager.js         # 主题管理器（演示用）
├── 📁 backend/                      # 后台系统
│   ├── app.py                       # Flask主应用
│   ├── database.py                  # 数据库模型
│   └── requirements.txt             # Python依赖
├── 📁 templates/admin/              # 后台页面模板
│   ├── login.html                   # 登录页面
│   ├── dashboard.html               # 管理面板
│   ├── settings.html                # 站点配置
│   ├── products.html                # 产品管理
│   └── ...                          # 其他管理页面
├── 📁 docs/                         # 项目文档
│   ├── README.md                    # 文档导航
│   ├── PROJECT_OVERVIEW.md          # 本文档
│   ├── frontend/                    # 前端文档
│   ├── backend/                     # 后端文档
│   └── ...                          # 其他文档
├── 📄 aistorm.db                    # SQLite数据库
├── 📄 theme-demo.html               # 主题演示页面
├── 📄 icons-demo.html               # 图标演示页面
├── 📄 Procfile                      # 部署配置
├── 📄 railway.json                  # Railway配置
├── 📄 runtime.txt                   # Python版本
└── 📄 deploy.sh                     # 部署脚本
```

## 🔌 API接口

### 公开API
- `GET /api/settings` - 获取站点配置
- `GET /api/products` - 获取所有产品
- `GET /api/products/<slug>` - 获取特定产品

### 管理API（需要身份验证）
- `POST /api/settings/update` - 更新站点配置
- `POST /api/products` - 创建产品
- `PUT /api/products/<id>` - 更新产品
- `DELETE /api/products/<id>` - 删除产品

## 🛠️ 技术栈

### 后端技术
- **框架**: Python Flask 2.3+
- **数据库**: SQLite + SQLAlchemy ORM
- **身份验证**: Flask Session + Werkzeug
- **跨域**: Flask-CORS
- **模板引擎**: Jinja2

### 前端技术
- **基础**: HTML5 + CSS3 + JavaScript ES6+
- **样式**: CSS Grid + Flexbox + CSS Variables
- **字体**: Google Fonts (Roboto)
- **图标**: 自定义SVG图标系统
- **响应式**: Mobile-first设计

### 部署技术
- **平台**: Railway / Render / Heroku
- **容器**: 支持Docker部署
- **CI/CD**: Git自动部署
- **域名**: 支持自定义域名

## 🔒 安全特性

- **密码安全**: Werkzeug密码哈希
- **会话管理**: Flask Session + 超时机制
- **权限验证**: 管理员权限检查
- **CSRF保护**: 表单令牌验证
- **环境变量**: 敏感信息配置

## 🚀 快速开始

### 本地开发
```bash
# 1. 克隆项目
git clone <repository-url>
cd AIStorm_Static_Website

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
cd backend && python3 app.py

# 4. 访问应用
# 前端: http://localhost:5001/
# 后台: http://localhost:5001/admin
```

### 默认登录凭据
- **用户名**: admin
- **密码**: admin123

⚠️ **重要**: 首次登录后请立即修改默认密码！

## 📱 访问地址

### 本地开发
- 前端网站: http://localhost:5001/
- 后台登录: http://localhost:5001/admin/login
- 后台首页: http://localhost:5001/admin
- 主题演示: http://localhost:5001/theme-demo.html
- 图标演示: http://localhost:5001/icons-demo.html

### 生产环境
部署后将获得类似以下的URL：
- 前端网站: https://your-app.railway.app/
- 后台管理: https://your-app.railway.app/admin

## 📋 功能特色

### 🎨 主题系统
- 4种预设主题（荧光青色、经典灰色、自然绿色、经典黑白）
- 12个可配置颜色变量
- 实时预览功能
- CSS变量动态应用

### 🔧 图标系统
- 23个统一设计图标
- 5种尺寸规格
- 6种颜色主题
- 3种动画效果

### 📦 产品管理
- 完整的CRUD操作
- 库存状态管理
- 价格配置（USDT + CNY）
- 产品图片管理

### 🌐 多语言支持
- 简体中文界面
- 统一术语规范
- 本地化内容

## 📞 技术支持

如有问题或建议，请：
1. 查看相关文档
2. 检查应用日志
3. 联系技术支持团队

## 📄 许可证

© 2025 AIStorm. 保留所有权利.

---

**AIStorm** - 让AI产品销售变得简单高效！ 🚀 