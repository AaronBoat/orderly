#!/bin/bash
# Orderly Telegram Bot 启动脚本
# 使用方法：chmod +x start.sh && ./start.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 Python
if ! command -v python3 &>/dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "⚙️  创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate

# 安装依赖
echo "⚙️  检查依赖..."
pip install --quiet -r requirements.txt

# 检查配置文件
if grep -q "REPLACE_WITH" config.yaml 2>/dev/null; then
    echo ""
    echo "❌ 请先编辑 config.yaml，填入以下内容："
    echo "   - telegram.bot_token"
    echo "   - gemini.api_key"
    echo ""
    echo "   使用命令：nano config.yaml"
    exit 1
fi

# 启动
if command -v screen &>/dev/null; then
    screen -dmS orderly-telebot bash -c "cd $SCRIPT_DIR && source venv/bin/activate && python3 main.py"
    echo ""
    echo "✅ Bot 已启动！"
    echo ""
    echo "  查看日志：  screen -r orderly-telebot"
    echo "  退出查看：  Ctrl+A 然后 D"
    echo "  实时日志：  tail -f $SCRIPT_DIR/bot.log"
    echo "  停止Bot：   screen -S orderly-telebot -X quit"
else
    echo "⚠️  未安装 screen，在前台运行（关闭终端会停止）"
    echo "   建议安装：sudo apt-get install screen"
    echo ""
    python3 main.py
fi
