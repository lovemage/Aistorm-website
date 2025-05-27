# AIStorm 后台管理系统

这是一个为AIStorm静态网站构建的完整后台管理系统，使用Flask + SQLAlchemy + SQLite技术栈。

## 🚀 功能特性

### 🔐 身份验证系统
- 用户名/密码登录验证
- 会话管理
- 管理员权限控制
- 密码修改功能

### 🎨 站点配置管理
- 网站名称和Logo设置
- 7种颜色主题配置（主色、辅色、背景色等）
- 联系方式管理（Telegram、WeChat、Email）
- USDT汇率设置
- SEO默认设置

### 📦 产品管理
- 产品CRUD操作（创建、读取、更新、删除）
- 库存状态管理
- 产品分类和排序
- 特色产品标记
- 产品特性列表管理
- SEO设置（每个产品独立的标题、描述、关键词）

### 📊 数据统计
- 产品总数统计
- 激活产品数量
- 特色产品数量
- 缺货产品数量

## 📁 项目结构

```
backend/
├── app.py              # Flask主应用
├── database.py         # 数据库模型定义
└── requirements.txt    # Python依赖包

templates/admin/
├── login.html          # 登录页面
├── dashboard.html      # 后台首页
├── settings.html       # 站点配置页面
├── products.html       # 产品列表页面
├── edit_product.html   # 编辑产品页面
├── new_product.html    # 添加产品页面
└── change_password.html # 修改密码页面

aistorm.db             # SQLite数据库文件
```

## 🛠️ 安装与运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用
```bash
cd backend
python3 app.py
```

### 3. 访问后台
打开浏览器访问：http://localhost:5001/admin

### 4. 默认登录凭据
- **用户名**: admin
- **密码**: admin123

⚠️ **重要**: 首次登录后请立即修改默认密码！

## 📋 使用指南

### 登录系统
1. 访问 http://localhost:5001/admin
2. 输入用户名和密码
3. 成功登录后会跳转到后台首页

### 站点配置
1. 点击"站点配置"菜单
2. 修改网站名称、Logo URL
3. 调整颜色主题（7种颜色配置）
4. 设置联系方式和汇率
5. 配置默认SEO设置
6. 点击"保存更改"

### 产品管理
1. 点击"产品管理"菜单查看所有产品
2. 点击"+ 添加新产品"创建新产品
3. 点击"编辑"按钮修改现有产品
4. 点击"删除"按钮删除产品（需确认）

### 修改密码
1. 在后台首页点击"修改密码"
2. 输入当前密码和新密码
3. 确认新密码
4. 点击"修改密码"保存

## 🔌 API 接口

### 公开API（无需身份验证）
- `GET /api/settings` - 获取站点配置
- `GET /api/products` - 获取所有激活的产品
- `GET /api/products/<slug>` - 获取特定产品

### 管理API（需要身份验证）
- `POST /api/settings/update` - 更新站点配置
- `POST /api/products` - 创建新产品
- `PUT /api/products/<id>` - 更新产品
- `DELETE /api/products/<id>` - 删除产品

## 🗄️ 数据库

使用 SQLite 数据库，包含两个主要表：
- `site_settings`: 站点配置信息
- `product`: 产品信息

数据库文件位于 `aistorm.db`，首次运行时会自动创建并初始化默认数据。

## 🔒 安全注意事项

1. **修改默认密码**: 首次登录后立即修改默认密码
2. **会话密钥**: 生产环境中修改`app.secret_key`
3. **HTTPS**: 生产环境中使用HTTPS
4. **数据库备份**: 定期备份SQLite数据库文件
5. **访问控制**: 确保后台管理界面不对外公开

## 🚀 扩展功能

可以考虑添加的功能：
- 多用户管理
- 操作日志记录
- 数据导入/导出
- 图片上传功能
- 邮件通知系统
- API访问令牌
- 数据库迁移工具

## 📞 技术支持

如有问题或建议，请联系开发团队。

---

© 2025 AIStorm. 保留所有权利. 