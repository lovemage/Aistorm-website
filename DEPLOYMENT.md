# AIStorm 后台管理系统 - 部署指南

本指南将帮助您将AIStorm后台管理系统部署到免费云服务器进行测试。

## 🚀 推荐的免费部署平台

### 1. Railway (推荐)
- **优点**: 简单易用，自动部署，免费额度充足
- **免费额度**: 每月500小时运行时间
- **网址**: https://railway.app

### 2. Render
- **优点**: 稳定可靠，支持自动SSL
- **免费额度**: 750小时/月，休眠后自动唤醒
- **网址**: https://render.com

### 3. Heroku
- **优点**: 老牌平台，文档丰富
- **免费额度**: 有限制，可能需要付费
- **网址**: https://heroku.com

## 📦 部署到Railway (推荐)

### 步骤1: 准备代码
1. 确保所有文件都已提交到Git仓库
2. 项目根目录应包含以下文件：
   - `requirements.txt`
   - `railway.json`
   - `Procfile`
   - `runtime.txt`

### 步骤2: 部署到Railway
1. 访问 https://railway.app
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择您的AIStorm项目仓库
6. Railway会自动检测Python项目并开始部署

### 步骤3: 配置环境变量
在Railway项目设置中添加以下环境变量：
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
PORT=8080
```

### 步骤4: 访问应用
部署完成后，Railway会提供一个公开URL，例如：
- 前端网站: `https://your-app.railway.app/`
- 后台管理: `https://your-app.railway.app/admin`

## 📦 部署到Render

### 步骤1: 创建Web Service
1. 访问 https://render.com
2. 注册并连接GitHub账号
3. 点击 "New" → "Web Service"
4. 选择您的GitHub仓库

### 步骤2: 配置部署设置
```
Name: aistorm-backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: cd backend && python app.py
```

### 步骤3: 设置环境变量
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
PORT=10000
```

## 📦 部署到Heroku

### 步骤1: 安装Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# 或下载安装包
# https://devcenter.heroku.com/articles/heroku-cli
```

### 步骤2: 登录并创建应用
```bash
heroku login
heroku create your-app-name
```

### 步骤3: 设置环境变量
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-super-secret-key-here
```

### 步骤4: 部署
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🔧 本地测试生产配置

在部署前，您可以本地测试生产环境配置：

```bash
# 设置环境变量
export FLASK_ENV=production
export SECRET_KEY=test-secret-key
export PORT=8080

# 启动应用
cd backend && python app.py
```

## 📋 部署检查清单

- [ ] 所有依赖包都在 `requirements.txt` 中
- [ ] 数据库文件路径正确配置
- [ ] 环境变量正确设置
- [ ] 静态文件路径配置正确
- [ ] 默认管理员账号可以登录
- [ ] API接口正常工作
- [ ] 前端页面正常显示

## 🔒 生产环境安全建议

1. **修改默认密码**: 部署后立即登录并修改默认管理员密码
2. **设置强密钥**: 使用强随机字符串作为SECRET_KEY
3. **启用HTTPS**: 大多数免费平台都自动提供SSL证书
4. **定期备份**: 定期下载数据库文件进行备份
5. **监控日志**: 关注应用日志，及时发现问题

## 🐛 常见问题解决

### 问题1: 应用无法启动
- 检查 `requirements.txt` 是否包含所有依赖
- 确认Python版本兼容性
- 查看部署日志中的错误信息

### 问题2: 数据库错误
- 确保SQLite数据库文件可写
- 检查数据库初始化是否成功
- 查看应用日志中的数据库相关错误

### 问题3: 静态文件404
- 确认静态文件路径配置正确
- 检查Flask静态文件服务配置
- 验证文件是否正确上传

### 问题4: 登录失败
- 确认数据库中有默认管理员账号
- 检查会话配置是否正确
- 验证密码哈希功能正常

## 📞 技术支持

如果在部署过程中遇到问题：

1. 查看平台的部署日志
2. 检查应用的运行日志
3. 参考平台官方文档
4. 联系技术支持团队

## 🔗 有用链接

- [Railway文档](https://docs.railway.app/)
- [Render文档](https://render.com/docs)
- [Heroku文档](https://devcenter.heroku.com/)
- [Flask部署指南](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

祝您部署顺利！🎉 