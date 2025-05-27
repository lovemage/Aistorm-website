# AIStorm 静态网站 + 后台管理系统

这是一个完整的AI产品销售网站，包含静态前端和功能完整的后台管理系统。

## 🌟 项目特色

### 前端网站
- 现代化响应式设计
- AI产品展示页面
- 多产品详情页面
- 联系方式集成

### 后台管理系统
- 🔐 用户身份验证（用户名/密码）
- 🎨 站点配置管理（颜色、Logo、联系方式）
- 📦 产品管理（CRUD操作、库存管理）
- 📊 数据统计面板
- 🔒 密码修改功能

## 🚀 快速开始

### 本地运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动后台服务
cd backend && python3 app.py

# 3. 访问网站
# 前端: http://localhost:5001/
# 后台: http://localhost:5001/admin
```

### 默认登录凭据
- **用户名**: admin
- **密码**: admin123

⚠️ **重要**: 首次登录后请立即修改默认密码！

## 🌐 部署到云服务器

### 快速部署
```bash
# 运行部署脚本
./deploy.sh
```

### 推荐平台
1. **Railway** (推荐) - https://railway.app
2. **Render** - https://render.com  
3. **Heroku** - https://heroku.com

详细部署指南请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📁 项目结构

```
AIStorm_Static_Website/
├── 📄 index.html                    # 前端主页
├── 📁 pages/                        # 产品详情页面
├── 📁 assets/                       # 静态资源
├── 📁 backend/                      # 后台系统
│   ├── app.py                       # Flask主应用
│   ├── database.py                  # 数据库模型
│   └── requirements.txt             # Python依赖
├── 📁 templates/admin/              # 后台页面模板
├── 📄 aistorm.db                    # SQLite数据库
├── 📄 Procfile                      # 部署配置
├── 📄 railway.json                  # Railway配置
├── 📄 runtime.txt                   # Python版本
├── 📄 deploy.sh                     # 部署脚本
├── 📄 DEPLOYMENT.md                 # 部署指南
└── 📄 BACKEND_README.md             # 后台系统文档
```

## 🔧 功能特性

### 后台管理功能
- ✅ 用户身份验证和会话管理
- ✅ 站点配置（7种颜色主题、Logo、联系方式）
- ✅ 产品管理（添加、编辑、删除、库存管理）
- ✅ 数据统计（产品数量、状态统计）
- ✅ 密码修改和安全设置
- ✅ RESTful API接口

### 前端网站功能
- ✅ 响应式设计，支持移动端
- ✅ 产品展示卡片
- ✅ 产品详情页面
- ✅ 联系方式展示
- ✅ 价格显示（USDT + CNY估算）

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

## 🔒 安全特性

- 密码哈希存储（Werkzeug）
- 会话管理和超时
- 管理员权限验证
- CSRF保护
- 环境变量配置

## 📱 访问地址

### 本地开发
- 前端网站: http://localhost:5001/
- 后台登录: http://localhost:5001/admin/login
- 后台首页: http://localhost:5001/admin
- API文档: http://localhost:5001/api/

### 生产环境
部署后将获得类似以下的URL：
- 前端网站: https://your-app.railway.app/
- 后台管理: https://your-app.railway.app/admin

## 🛠️ 技术栈

### 后端
- **框架**: Python Flask
- **数据库**: SQLite + SQLAlchemy ORM
- **身份验证**: Flask Session + Werkzeug
- **跨域**: Flask-CORS

### 前端
- **技术**: HTML5 + CSS3 + JavaScript
- **设计**: 响应式布局
- **图标**: 自定义图标系统

### 部署
- **平台**: Railway / Render / Heroku
- **容器**: 支持Docker部署
- **CI/CD**: Git自动部署

## 📋 部署检查清单

- [ ] 所有文件已提交到Git仓库
- [ ] requirements.txt包含所有依赖
- [ ] 环境变量正确配置
- [ ] 数据库初始化正常
- [ ] 静态文件路径正确
- [ ] API接口正常工作
- [ ] 默认管理员账号可登录
- [ ] 前端页面正常显示

## 🐛 故障排除

### 常见问题
1. **端口占用**: 修改PORT环境变量
2. **数据库错误**: 检查SQLite文件权限
3. **静态文件404**: 验证文件路径配置
4. **登录失败**: 确认数据库初始化成功

### 获取帮助
- 查看 [BACKEND_README.md](BACKEND_README.md) 了解后台系统详情
- 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 了解部署指南
- 检查应用日志获取错误信息

## 📞 技术支持

如有问题或建议，请：
1. 查看相关文档
2. 检查应用日志
3. 联系技术支持团队

## 📄 许可证

© 2025 AIStorm. 保留所有权利.

---

**AIStorm** - 让AI产品销售变得简单高效！ 🚀 