#!/bin/bash

# AIStorm 后台管理系统 - 快速部署脚本

echo "🚀 AIStorm 后台管理系统 - 部署准备"
echo "=================================="

# 检查Git状态
echo "📋 检查Git状态..."
if ! git status &>/dev/null; then
    echo "❌ 错误: 当前目录不是Git仓库"
    echo "请先运行: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# 检查必要文件
echo "📋 检查必要文件..."
required_files=("requirements.txt" "Procfile" "railway.json" "runtime.txt")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ 缺少文件: $file"
        exit 1
    fi
    echo "✅ $file"
done

# 检查Python依赖
echo "📋 检查Python依赖..."
if [[ ! -f "backend/app.py" ]]; then
    echo "❌ 错误: 找不到backend/app.py"
    exit 1
fi

# 测试本地应用
echo "🧪 测试本地应用..."
cd backend
if ! python -c "import flask, flask_sqlalchemy, flask_cors"; then
    echo "❌ 错误: 缺少必要的Python包"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi
cd ..

echo "✅ 所有检查通过！"
echo ""

# 显示部署选项
echo "🌐 选择部署平台:"
echo "1) Railway (推荐)"
echo "2) Render"
echo "3) Heroku"
echo "4) 仅准备文件，手动部署"
echo ""

read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo "🚂 Railway 部署指南:"
        echo "1. 访问 https://railway.app"
        echo "2. 使用GitHub登录"
        echo "3. 点击 'New Project' → 'Deploy from GitHub repo'"
        echo "4. 选择此仓库"
        echo "5. 设置环境变量:"
        echo "   FLASK_ENV=production"
        echo "   SECRET_KEY=$(openssl rand -base64 32)"
        echo "   PORT=8080"
        ;;
    2)
        echo "🎨 Render 部署指南:"
        echo "1. 访问 https://render.com"
        echo "2. 连接GitHub账号"
        echo "3. 创建新的Web Service"
        echo "4. 配置:"
        echo "   Build Command: pip install -r requirements.txt"
        echo "   Start Command: cd backend && python app.py"
        echo "5. 设置环境变量:"
        echo "   FLASK_ENV=production"
        echo "   SECRET_KEY=$(openssl rand -base64 32)"
        echo "   PORT=10000"
        ;;
    3)
        echo "🟣 Heroku 部署指南:"
        echo "1. 安装Heroku CLI"
        echo "2. 运行以下命令:"
        echo "   heroku login"
        echo "   heroku create your-app-name"
        echo "   heroku config:set FLASK_ENV=production"
        echo "   heroku config:set SECRET_KEY=$(openssl rand -base64 32)"
        echo "   git push heroku main"
        ;;
    4)
        echo "📁 文件已准备完毕，可以手动部署"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🔑 默认登录凭据:"
echo "用户名: admin"
echo "密码: admin123"
echo ""
echo "⚠️  重要提醒:"
echo "1. 部署后立即修改默认密码"
echo "2. 确保设置了强随机的SECRET_KEY"
echo "3. 检查所有功能是否正常工作"
echo ""
echo "📚 详细部署指南请查看: DEPLOYMENT.md"
echo ""
echo "🎉 祝您部署顺利！" 