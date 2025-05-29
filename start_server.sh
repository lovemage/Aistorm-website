#!/bin/bash

# AIStorm 服务器启动脚本
echo "🚀 启动 AIStorm 后端服务器..."

# 设置环境变量
export TELEGRAM_BOT_TOKEN="7732727026:AAEKwiUrc0q3AYOoDrlONbj-m5UIQ2MpvqA"
export TELEGRAM_CHAT_ID="7935635650"
export OXAPAY_SECRET_KEY="URXMY9-VHVPGK-DA4HEC-2EXI3S"
export SECRET_KEY="aistorm-production-secret-2025"
export PORT="5001"

# 显示配置状态
echo "📋 环境变量配置:"
echo "  - TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:0:10}..."
echo "  - TELEGRAM_CHAT_ID: $TELEGRAM_CHAT_ID"
echo "  - OXAPAY_SECRET_KEY: ${OXAPAY_SECRET_KEY:0:6}..."
echo "  - PORT: $PORT"

# 停止现有进程
echo "🛑 停止现有进程..."
pkill -f "python3 backend/app.py" 2>/dev/null || true
sleep 2

# 启动服务器
echo "🔥 启动后端服务器..."
cd "$(dirname "$0")"
python3 backend/app.py 