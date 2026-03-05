#!/bin/bash
# 查看最近的 Bot 日志（包含 Topic ID 信息）

echo "=========================================="
echo "  最近的消息和 Topic ID"
echo "=========================================="
echo ""
echo "正在查看 screen 会话日志..."
echo "按 Ctrl+C 退出查看"
echo ""
echo "=========================================="
echo ""

# 使用 script 命令捕获 screen 输出
screen -r telegram-bot
