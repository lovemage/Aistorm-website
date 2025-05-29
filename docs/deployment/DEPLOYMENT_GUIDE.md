# 🚀 AIStorm 部署指南

## ⚠️ Railway 部署问题修复

### 问题解决
如果遇到 "The executable `cd` could not be found" 错误，我们已经提供了修复方案：

1. **新增 `start.py` 启动脚本** - 避免shell命令问题
2. **更新 `Procfile`** - 使用简单的Python命令
3. **修复 `railway.json`** - 正确配置启动命令

### 部署前测试
```bash
# 测试依赖安装
python test_dependencies.py

# 测试启动脚本
python start.py
```

## 📋 部署前准备

### 1. 环境变量配置

在部署平台中设置以下环境变量：

```bash
# 必需的环境变量
TELEGRAM_BOT_TOKEN=你的-telegram-bot-token
TELEGRAM_CHAT_ID=你的-telegram-chat-id  
OXAPAY_SECRET_KEY=你的-oxapay-api-key
SECRET_KEY=你的-flask-密钥

# 可选环境变量
FLASK_ENV=production
PORT=5001
DEBUG=False
```

### 2. 依赖包安装

确保安装所有必需的Python包：

```bash
pip install -r requirements.txt
```

## 🌐 各平台部署指南

### Railway 部署

1. **推送代码到GitHub**：
   ```bash
   git add .
   git commit -m "deploy: 修复Railway部署问题"
   git push origin main
   ```

2. **在Railway中配置环境变量**：
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `OXAPAY_SECRET_KEY`
   - `SECRET_KEY`

3. **部署配置文件**：
   - `requirements.txt` - Python依赖 ✅
   - `runtime.txt` - Python版本 ✅
   - `Procfile` - 启动命令 ✅ (已修复)
   - `railway.json` - Railway配置 ✅ (已修复)
   - `start.py` - 启动脚本 ✅ (新增)

### Heroku 部署

1. **安装Heroku CLI**
2. **登录Heroku**：
   ```bash
   heroku login
   ```

3. **创建应用**：
   ```bash
   heroku create your-app-name
   ```

4. **设置环境变量**：
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=你的-token
   heroku config:set TELEGRAM_CHAT_ID=你的-chat-id
   heroku config:set OXAPAY_SECRET_KEY=你的-api-key
   heroku config:set SECRET_KEY=你的-密钥
   ```

5. **部署**：
   ```bash
   git push heroku main
   ```

### Vercel 部署

1. **安装Vercel CLI**：
   ```bash
   npm i -g vercel
   ```

2. **配置vercel.json**：
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "start.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/start.py"
       }
     ]
   }
   ```

3. **部署**：
   ```bash
   vercel --prod
   ```

### DigitalOcean App Platform

1. **连接GitHub仓库**
2. **配置环境变量**
3. **选择Python buildpack**
4. **设置启动命令**：`python start.py`

## 🐳 Docker 部署

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5001

# 设置环境变量
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 启动应用
CMD ["python", "start.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  aistorm:
    build: .
    ports:
      - "5001:5001"
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
      - OXAPAY_SECRET_KEY=${OXAPAY_SECRET_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
```

## 🔧 常见部署问题解决

### 1. ModuleNotFoundError: No module named 'requests'

**解决方案**：
- 确保 `requirements.txt` 包含 `requests==2.31.0`
- 重新部署应用

### 2. The executable 'cd' could not be found (已修复)

**解决方案**：
- 使用新的 `start.py` 启动脚本
- 更新的 `Procfile`: `web: python start.py`
- 更新的 `railway.json` 配置

### 3. Port already in use

**解决方案**：
```bash
# 杀死占用端口的进程
lsof -ti:5001 | xargs kill -9

# 或者使用不同端口
export PORT=5002
```

### 4. 环境变量未设置

**解决方案**：
- 检查环境变量是否正确设置
- 确保变量名拼写正确
- 在本地测试时使用 `.env` 文件

### 5. 数据库初始化失败

**解决方案**：
```bash
# 删除现有数据库文件
rm aistorm.db

# 重新启动应用让它重新创建数据库
python start.py
```

## 📊 部署后验证

### 1. 健康检查

访问以下端点验证服务正常：
```
GET /api/products
GET /api/settings
POST /api/test-telegram
```

### 2. 功能测试

1. **产品列表加载**
2. **订单创建**
3. **支付流程**
4. **Telegram通知**

### 3. 日志监控

检查应用日志确保没有错误：
```bash
# Railway
railway logs

# Heroku  
heroku logs --tail

# Docker
docker logs container_name
```

## 🛡️ 生产环境安全

1. **使用HTTPS**
2. **设置强随机SECRET_KEY**
3. **定期轮换API密钥**
4. **启用访问日志**
5. **监控异常访问**

## 🧪 部署前测试清单

- [ ] 运行 `python test_dependencies.py` 
- [ ] 测试 `python start.py` 启动正常
- [ ] 检查环境变量配置
- [ ] 验证API端点响应
- [ ] 测试Telegram通知功能

## 📞 技术支持

如遇到部署问题，请检查：
1. 依赖包是否完整安装
2. 环境变量是否正确配置
3. 端口是否被正确绑定
4. 应用日志中的错误信息

---
最后更新：2025年5月 - Railway部署问题修复版本 