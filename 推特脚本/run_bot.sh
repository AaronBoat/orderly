#!/bin/bash
# Orderly 推特蹭热点机器人 - 快速启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=================================="
echo "Orderly 推特蹭热点机器人"
echo "=================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.10 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 检查并安装依赖..."
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  警告：未找到 .env 文件"
    echo "请先复制 .env.example 为 .env 并填入你的 API 凭证："
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env  # 或使用其他编辑器"
    echo ""
    exit 1
fi

echo "✅ 环境配置完成"
echo ""
echo "🚀 开始运行机器人..."
echo "=================================="
echo ""

# 运行脚本
python3 orderly_rub_heat_bot.py

echo ""
echo "=================================="
echo "✅ 执行完成"
echo "=================================="
