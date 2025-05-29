#!/bin/bash

# AIStorm 后端服务器启动脚本
echo "🚀 启动 AIStorm 后端服务器..."

# 检查.env文件是否存在
if [ -f ".env" ]; then
    echo "📋 从.env文件加载环境变量..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️ 未找到.env文件，请复制env.example为.env并配置API密钥"
    echo "ℹ️ 当前将使用系统环境变量（如果有）"
fi

# 显示配置状态（隐藏敏感信息）
echo "📋 环境变量配置状态:"
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "  - TELEGRAM_BOT_TOKEN: 已配置"
else
    echo "  - TELEGRAM_BOT_TOKEN: ❌ 未配置"
fi

if [ -n "$TELEGRAM_CHAT_ID" ]; then
    echo "  - TELEGRAM_CHAT_ID: $TELEGRAM_CHAT_ID"
else
    echo "  - TELEGRAM_CHAT_ID: ❌ 未配置"
fi

if [ -n "$OXAPAY_SECRET_KEY" ]; then
    echo "  - OXAPAY_SECRET_KEY: 已配置"
else
    echo "  - OXAPAY_SECRET_KEY: ❌ 未配置"
fi

echo "  - PORT: ${PORT:-5001}"

# 停止现有进程
echo "🛑 停止现有进程..."
pkill -f "python3 backend/app.py" 2>/dev/null || true

# 等待进程完全停止
sleep 2

# 启动后端服务器
echo "🔥 启动后端服务器..."
python3 backend/app.py 