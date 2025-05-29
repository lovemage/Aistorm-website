# 📦 AIStorm 部署指南

## 📋 目录
- [Railway 部署](#railway-部署)
- [Railway 部署问题修复](#railway-部署问题修复)
- [常规部署指南](#常规部署指南)
- [安全配置](#安全配置)
- [故障排除](#故障排除)

---

## 🚀 Railway 部署

### 快速部署步骤

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "准备部署"
   git push origin main
   ```

2. **在 Railway 创建项目**
   - 访问 [Railway.app](https://railway.app)
   - 连接 GitHub 仓库
   - 选择 AIStorm 项目

3. **配置环境变量**
   ```
   TELEGRAM_BOT_TOKEN=你的机器人TOKEN
   TELEGRAM_CHAT_ID=你的聊天ID
   OXAPAY_SECRET_KEY=你的OxaPay密钥
   SECRET_KEY=你的Flask密钥
   FLASK_ENV=production
   ```

4. **部署配置文件**
   - `Procfile`: `python start.py`
   - `railway.json`: 健康检查配置
   - `requirements.txt`: Python依赖

### Railway 配置文件

#### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python start.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 120,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

#### Procfile
```
web: python start.py
```

---

## 🔧 Railway 部署问题修复

### 已修复的问题

#### 1. 500 内部服务器错误
**问题**: Railway部署后出现500错误，健康检查失败
**修复**: 
- 修复 Flask 重启时的路径问题
- 在生产环境中禁用调试模式
- 使用 `datetime.now(timezone.utc)` 替代已弃用的 `datetime.utcnow()`

#### 2. "cd command not found" 错误
**问题**: Railway 无法执行 shell 命令
**修复**:
- 使用 Python 启动脚本 `start.py` 替代 shell 命令
- 简化 Procfile 配置

#### 3. 依赖安装问题
**问题**: "ModuleNotFoundError: No module named 'requests'"
**修复**:
- 简化 `requirements.txt`，使用版本范围
- 移除不必要的依赖和注释

#### 4. 健康检查失败
**问题**: 健康检查超时，应用无法启动
**修复**:
- 健康检查路径改为根路径 `/`
- 调整超时和重试参数
- 优化启动脚本路径配置

### 修复的文件

#### start.py 启动脚本
```python
#!/usr/bin/env python3
"""
AIStorm 应用启动脚本
用于Railway等部署平台的简化启动
"""

import os
import sys
import traceback

def main():
    try:
        print("🚀 AIStorm 应用启动中...")
        
        # 检查环境变量
        required_env_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'OXAPAY_SECRET_KEY']
        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ 缺少环境变量: {', '.join(missing_vars)}")
        else:
            print("✅ 所有必需的环境变量都已设置")
        
        # 添加backend目录到Python路径
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        
        # 保持工作目录在项目根目录
        print(f"📁 保持工作目录: {os.getcwd()}")
        
        # 导入应用
        from app import app, init_db
        
        # 初始化数据库
        with app.app_context():
            init_db(app)
        
        # 启动应用
        port = int(os.environ.get('PORT', 5001))
        flask_env = os.environ.get('FLASK_ENV', 'development')
        debug = flask_env == 'development'
        
        app.run(debug=debug, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"💥 启动失败: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
```

#### requirements.txt 优化
```txt
# AIStorm 支付系统核心依赖
Flask>=2.3.0,<3.0.0
Flask-SQLAlchemy>=3.0.0,<4.0.0
Flask-CORS>=4.0.0,<5.0.0
requests>=2.31.0,<3.0.0
Werkzeug>=2.3.0,<3.0.0
SQLAlchemy>=2.0.0,<3.0.0
python-dotenv>=1.0.0,<2.0.0
```

---

## 📚 常规部署指南

### 支持的平台
- **Railway** (推荐)
- **Render**
- **Heroku**
- **自托管服务器**

### 环境要求
- Python 3.8+
- SQLite (内置)
- 2GB RAM (推荐)
- 1GB 存储空间

### 部署前检查
- [ ] 所有代码已提交到 Git
- [ ] 环境变量已配置
- [ ] 数据库可正常初始化
- [ ] 静态文件路径正确
- [ ] API 端点可访问

### 部署后验证
1. **前端检查**
   - 访问首页是否正常显示
   - 产品页面是否加载
   - 静态资源是否可访问

2. **后台检查**
   - 管理员登录是否正常
   - 产品管理功能是否工作
   - API 接口是否响应

3. **支付功能检查**
   - Telegram 通知是否正常
   - OxaPay 集成是否工作
   - 订单创建是否成功

---

## 🔒 安全配置

### 环境变量安全
- 使用强密码的 `SECRET_KEY`
- 定期轮换 API 密钥
- 限制环境变量访问权限

### 生产环境设置
```bash
FLASK_ENV=production          # 禁用调试模式
SECRET_KEY=your-secret-key    # 强密码
DEBUG=false                   # 禁用调试
```

### 安全检查清单
- [ ] 默认管理员密码已修改
- [ ] 生产环境禁用调试模式
- [ ] API 密钥安全存储
- [ ] HTTPS 证书配置
- [ ] 访问日志监控

---

## 🐛 故障排除

### 常见部署问题

#### 1. 应用无法启动
**症状**: 部署后显示错误页面
**解决方案**:
```bash
# 检查启动日志
railway logs

# 验证环境变量
railway variables

# 重新部署
railway up --detach
```

#### 2. 静态文件404
**症状**: CSS/JS/图片无法加载
**解决方案**:
- 检查文件路径配置
- 验证 Flask 静态文件设置
- 确认文件已正确提交

#### 3. 数据库错误
**症状**: SQLite 相关错误
**解决方案**:
- 检查数据库文件权限
- 验证初始化脚本
- 重新创建数据库

#### 4. 环境变量问题
**症状**: 配置相关错误
**解决方案**:
```bash
# Railway 设置环境变量
railway variables set TELEGRAM_BOT_TOKEN=your-token
railway variables set TELEGRAM_CHAT_ID=your-chat-id
railway variables set OXAPAY_SECRET_KEY=your-key
railway variables set SECRET_KEY=your-secret
railway variables set FLASK_ENV=production
```

### 调试工具
- 查看部署日志
- 检查健康检查状态
- 验证环境变量设置
- 测试 API 端点

### 性能优化
- 启用 Gzip 压缩
- 优化静态资源
- 配置缓存策略
- 监控资源使用

---

## 📞 获取帮助

### 部署支持
- Railway 官方文档: https://docs.railway.app
- GitHub Issues: 项目问题追踪
- 技术支持: 联系开发团队

### 有用的链接
- [Railway 部署教程](https://docs.railway.app/deploy/deployments)
- [Flask 生产部署指南](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [SQLite 生产使用](https://sqlite.org/whentouse.html)

---

**状态**: ✅ 所有部署问题已修复，准备生产环境使用  
**最后更新**: 2025-05-29 