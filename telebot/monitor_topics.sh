#!/bin/bash
# 实时监控 Bot 并显示 Topic ID

echo "🔍 正在监控 Bot 输出..."
echo "📝 请在不同的 Topic 中发送测试消息"
echo "💡 每条消息会显示其 Topic ID"
echo ""
echo "按 Ctrl+C 停止监控"
echo "=========================================="
echo ""

cd /Users/aaron/orderly打工/telebot

# 重启 Bot 并直接显示输出
screen -X -S telegram-bot quit 2>/dev/null
pkill -9 -f "python.*main.py" 2>/dev/null
sleep 1

echo "🚀 启动 Bot（前台模式）..."
echo ""

python3 main.py 2>&1 | grep --line-buffered -E "(📌|Topic ID|收到新消息|翻译|转发)" || python3 main.py
