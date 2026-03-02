#!/bin/bash
# Telegram Bot 启动和监控脚本

BOT_DIR="/Users/aaron/orderly打工/telebot"
SCREEN_NAME="telegram-bot"

cd "$BOT_DIR" || exit 1

# 检查配置文件是否存在
if [ ! -f "config.yaml" ]; then
    echo "❌ 错误：config.yaml 不存在"
    echo "请先运行: cp config.yaml.example config.yaml"
    echo "然后编辑 config.yaml 填入你的配置"
    exit 1
fi

# 检查是否已经在运行
if screen -list | grep -q "$SCREEN_NAME"; then
    echo "⚠️  Bot 已经在 screen 会话中运行"
    echo "查看日志: screen -r $SCREEN_NAME"
    exit 0
fi

# 检查 Python 进程
if pgrep -f "python.*main.py" > /dev/null; then
    echo "⚠️  Bot 进程已在运行"
    ps aux | grep "python.*main.py" | grep -v grep
    exit 0
fi

# 启动 Bot
echo "🚀 启动 Telegram Bot..."
screen -dmS "$SCREEN_NAME" python3 main.py

sleep 2

# 检查是否成功启动
if screen -list | grep -q "$SCREEN_NAME"; then
    echo "✅ Bot 已成功启动在 screen 会话中"
    echo ""
    echo "📋 查看日志: screen -r $SCREEN_NAME"
    echo "📋 退出查看（不停止Bot）: 按 Ctrl+A 然后按 D"
    echo "📋 停止 Bot: screen -X -S $SCREEN_NAME quit"
else
    echo "❌ Bot 启动失败"
    exit 1
fi
