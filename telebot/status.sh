#!/bin/bash
# Bot 状态监控脚本

BOT_DIR="/Users/aaron/orderly打工/telebot"
SCREEN_NAME="telegram-bot"

echo "===================================="
echo "  Telegram Bot 状态监控"
echo "===================================="
echo ""

# 检查配置文件
echo "📁 配置文件状态："
if [ -f "$BOT_DIR/config.yaml" ]; then
    echo "   ✅ config.yaml 存在"
else
    echo "   ❌ config.yaml 不存在"
fi
echo ""

# 检查 screen 会话
echo "🖥️  Screen 会话："
if screen -list | grep -q "$SCREEN_NAME"; then
    echo "   ✅ Screen 会话存在"
    screen -list | grep "$SCREEN_NAME"
else
    echo "   ❌ 没有 screen 会话"
fi
echo ""

# 检查进程
echo "⚙️  Python 进程："
if pgrep -f "python.*main.py" > /dev/null; then
    echo "   ✅ Bot 进程运行中"
    ps aux | grep "python.*main.py" | grep -v grep | awk '{print "   PID: "$2" | CPU: "$3"% | MEM: "$4"%"}'
else
    echo "   ❌ Bot 进程未运行"
fi
echo ""

# 提供操作建议
echo "===================================="
echo "📋 可用命令："
echo "   启动: ./start_bot.sh 或 bash start_bot.sh"
echo "   查看: screen -r $SCREEN_NAME"
echo "   停止: screen -X -S $SCREEN_NAME quit"
echo "   测试: python3 test_bot.py"
echo "===================================="
