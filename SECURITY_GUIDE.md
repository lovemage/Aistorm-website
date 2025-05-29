# 🛡️ AIStorm 安全配置指南

## ⚠️ 重要安全警告

**请勿将真实的API密钥和Token提交到公开的Git仓库！**

## 🔧 安全配置步骤

### 1. 设置环境变量

#### 方法一：使用.env文件（推荐）
```bash
# 复制示例文件
cp env.example .env

# 编辑.env文件，填入真实的API密钥
nano .env
```

#### 方法二：手动设置环境变量
```bash
export TELEGRAM_BOT_TOKEN="你的-telegram-bot-token"
export TELEGRAM_CHAT_ID="你的-telegram-chat-id"
export OXAPAY_SECRET_KEY="你的-oxapay-api-key"
export SECRET_KEY="你的-flask-密钥"
```

### 2. 启动服务器
```bash
# 使用安全的启动脚本
./start_server.sh
```

## 🔍 敏感信息检查清单

在提交代码前，请确保以下文件中**没有**包含真实的API密钥：

- [ ] `backend/app.py`
- [ ] `start_server.sh`
- [ ] 任何`.md`文档文件
- [ ] 任何配置文件

## 📁 安全文件配置

### .gitignore
确保以下文件不会被提交到Git：
```
.env
.env.local
.env.production
*.env
*.db
config/secrets.json
```

### 环境变量文件
- ✅ `env.example` - 示例文件（不包含真实密钥）
- ❌ `.env` - 实际配置文件（包含真实密钥，应被gitignore）

## 🚨 如果密钥已经泄露

如果您的API密钥已经被推送到GitHub，请立即：

1. **撤销现有密钥**：
   - 到Telegram BotFather撤销旧Token
   - 到OxaPay控制台生成新的API密钥

2. **生成新密钥**：
   - 获取新的Telegram Bot Token
   - 获取新的OxaPay API密钥

3. **清理Git历史**（如果需要）：
   ```bash
   # 警告：这会重写Git历史
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch backend/app.py' \
   --prune-empty --tag-name-filter cat -- --all
   ```

4. **更新配置**：
   - 在`.env`文件中设置新密钥
   - 重新部署应用

## 🔐 生产环境部署

在生产环境中：
- 使用环境变量或密钥管理服务
- 启用HTTPS
- 使用强随机SECRET_KEY
- 定期轮换API密钥
- 启用访问日志和监控

## 📞 联系支持

如有安全问题，请联系开发团队。

---
最后更新：2025年5月 