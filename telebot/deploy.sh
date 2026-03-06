#!/bin/bash
# ============================================================
# Orderly Telegram 翻译机器人 — 一键部署脚本
# 使用方法：chmod +x deploy.sh && ./deploy.sh
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════╗"
echo "║   Orderly Telegram Bot — 一键部署脚本        ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# ── 1. 检查系统依赖 ─────────────────────────────────────────
echo -e "${YELLOW}[1/5] 检查系统依赖...${NC}"

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ 未找到 python3，正在安装...${NC}"
    sudo apt-get update -qq && sudo apt-get install -y python3 python3-pip python3-venv
else
    PY_VER=$(python3 --version)
    echo -e "${GREEN}✅ $PY_VER 已安装${NC}"
fi

if ! command -v screen &>/dev/null; then
    echo -e "${YELLOW}⚙️  安装 screen...${NC}"
    sudo apt-get install -y screen
fi

echo -e "${GREEN}✅ 系统依赖检查完成${NC}"

# ── 2. 创建虚拟环境 ─────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/5] 创建 Python 虚拟环境...${NC}"

DEPLOY_DIR="$HOME/orderly-telebot"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ 虚拟环境已创建：$DEPLOY_DIR/venv${NC}"
else
    echo -e "${GREEN}✅ 虚拟环境已存在，跳过创建${NC}"
fi

source venv/bin/activate

# ── 3. 安装 Python 依赖 ─────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/5] 安装 Python 依赖包...${NC}"

pip install --quiet --upgrade pip
pip install --quiet \
    "python-telegram-bot==21.0" \
    "google-generativeai>=0.3.0" \
    "PyYAML>=6.0"

echo -e "${GREEN}✅ 依赖安装完成${NC}"

# ── 4. 写入主程序文件 ────────────────────────────────────────
echo ""
echo -e "${YELLOW}[4/5] 写入程序文件...${NC}"

# ---------- main.py ----------
cat > "$DEPLOY_DIR/main.py" << 'MAIN_PY'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 群公告 AI 翻译转发机器人
监听源群组消息，通过 Gemini API 翻译为中文后转发到目标群组
"""

import asyncio
import logging
from collections import deque
from typing import Optional
import yaml
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

recent_message_ids = deque(maxlen=50)

TRANSLATION_PROMPT = """你是一个专业的翻译官。请将输入的 Telegram 消息翻译成中文。要求：保持原有的 Emoji 位置，保留专有名词（如项目名、代码），语言风格要自然、符合中文社交媒体习惯。仅返回翻译后的文本，不要有任何解释说明。"""


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.bot_token = config['telegram']['bot_token']
        self.source_chat_id = int(config['telegram']['source_chat_id'])
        self.target_chat_id = int(config['telegram']['target_chat_id'])
        self.allowed_topics = config['telegram'].get('allowed_topics', [])
        self.allowed_topics_lower = [str(t).lower() for t in self.allowed_topics] if self.allowed_topics else []
        self.gemini_api_key = config['gemini']['api_key']
        self.gemini_model = config['gemini']['model_name']
        self.language = config['settings']['language']
        self.mode = config['settings'].get('mode', 'translate')


class GeminiTranslator:
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.max_retries = 3

    async def translate(self, text: str) -> Optional[str]:
        for attempt in range(self.max_retries):
            try:
                full_prompt = f"{TRANSLATION_PROMPT}\n\n原文：\n{text}"
                response = await asyncio.to_thread(self.model.generate_content, full_prompt)
                translated_text = response.text.strip()
                logger.info(f"翻译成功 (尝试 {attempt + 1}/{self.max_retries})")
                return translated_text
            except Exception as e:
                logger.error(f"翻译失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("翻译失败，已达到最大重试次数")
                    return None


class TranslationBot:
    def __init__(self, config: Config):
        self.config = config
        self.translator = GeminiTranslator(config.gemini_api_key, config.gemini_model)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message or update.channel_post
        if not message:
            return
        if message.chat_id != self.config.source_chat_id:
            logger.debug(f"忽略非源群组消息: {message.chat_id}")
            return

        topic_id = message.message_thread_id
        if topic_id:
            logger.info(f"📌 消息来自 Topic ID: {topic_id}")
        else:
            logger.info(f"📌 消息不在任何 Topic 中（可能是主群组消息）")

        if self.config.allowed_topics_lower:
            if topic_id:
                if str(topic_id) in [str(t) for t in self.config.allowed_topics]:
                    logger.info(f"✅ Topic ID {topic_id} 在允许列表中")
                else:
                    logger.info(f"⏭️ Topic ID {topic_id} 不在允许列表中，跳过")
                    return
            else:
                logger.info(f"⏭️ 消息不在任何 Topic 中，且配置了 Topic 过滤，跳过")
                return

        if message.message_id in recent_message_ids:
            logger.info(f"消息 {message.message_id} 已处理，跳过")
            return
        recent_message_ids.append(message.message_id)

        logger.info(f"收到新消息 ID: {message.message_id} from Chat: {message.chat_id}")
        if message.text:
            logger.info(f"📝 消息文本: {message.text}")
        elif message.caption:
            logger.info(f"📝 消息说明: {message.caption}")

        if self.config.mode == "monitor":
            logger.info("✅ 消息已记录到日志（监听模式）")
            return

        text_to_translate = None
        if message.text:
            text_to_translate = message.text
        elif message.caption:
            text_to_translate = message.caption

        if not text_to_translate and not (message.photo or message.video or message.document):
            logger.info("消息无内容，跳过")
            return
        if not text_to_translate:
            logger.info("消息无文本内容，直接转发媒体")
            await self._forward_message(message, context)
            return

        translated_text = await self.translator.translate(text_to_translate)
        if not translated_text:
            logger.error("翻译失败，转发原消息")
            await self._forward_message(message, context)
            return
        await self._send_translated_message(message, translated_text, context)

    async def _forward_message(self, message, context):
        try:
            if message.photo:
                await context.bot.send_photo(chat_id=self.config.target_chat_id, photo=message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                await context.bot.send_video(chat_id=self.config.target_chat_id, video=message.video.file_id, caption=message.caption or "")
            elif message.document:
                await context.bot.send_document(chat_id=self.config.target_chat_id, document=message.document.file_id, caption=message.caption or "")
            elif message.text:
                await context.bot.send_message(chat_id=self.config.target_chat_id, text=message.text)
            logger.info(f"消息 {message.message_id} 已直接转发")
        except Exception as e:
            logger.error(f"转发消息失败: {e}")

    async def _send_translated_message(self, message, translated_text, context):
        try:
            max_length = 4000
            text_chunks = self._split_text(translated_text, max_length)
            if message.photo:
                await context.bot.send_photo(chat_id=self.config.target_chat_id, photo=message.photo[-1].file_id, caption=text_chunks[0])
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)
                    await context.bot.send_message(chat_id=self.config.target_chat_id, text=chunk)
            elif message.video:
                await context.bot.send_video(chat_id=self.config.target_chat_id, video=message.video.file_id, caption=text_chunks[0])
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)
                    await context.bot.send_message(chat_id=self.config.target_chat_id, text=chunk)
            elif message.document:
                await context.bot.send_document(chat_id=self.config.target_chat_id, document=message.document.file_id, caption=text_chunks[0])
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)
                    await context.bot.send_message(chat_id=self.config.target_chat_id, text=chunk)
            else:
                for chunk in text_chunks:
                    await context.bot.send_message(chat_id=self.config.target_chat_id, text=chunk)
                    if len(text_chunks) > 1:
                        await asyncio.sleep(0.5)
            logger.info(f"消息 {message.message_id} 翻译转发成功")
        except Exception as e:
            logger.error(f"发送翻译消息失败: {e}")
            await self._forward_message(message, context)

    @staticmethod
    def _split_text(text: str, max_length: int) -> list:
        if len(text) <= max_length:
            return [text]
        chunks = []
        current_chunk = ""
        for line in text.split('\n'):
            if len(line) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                for i in range(0, len(line), max_length):
                    chunks.append(line[i:i + max_length])
            elif len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"更新 {update} 引发错误：{context.error}")


def main():
    try:
        config = Config()
        logger.info("配置加载成功")
        bot = TranslationBot(config)
        application = Application.builder().token(config.bot_token).build()
        application.add_handler(MessageHandler(filters.ChatType.GROUPS | filters.ChatType.CHANNEL, bot.handle_message))
        application.add_error_handler(error_handler)
        logger.info("机器人启动中...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except FileNotFoundError:
        logger.error("配置文件 config.yaml 不存在，请先创建配置文件")
    except Exception as e:
        logger.error(f"启动失败: {e}")


if __name__ == "__main__":
    main()
MAIN_PY

# ---------- config.yaml ----------
cat > "$DEPLOY_DIR/config.yaml" << 'CONFIG_YAML'
telegram:
  bot_token: "REPLACE_WITH_BOT_TOKEN"
  source_chat_id: -1002011191127
  allowed_topics:
    - 100388
    - 1699
  target_chat_id: -1002266428094

gemini:
  api_key: "REPLACE_WITH_GEMINI_API_KEY"
  model_name: "gemini-2.5-flash"

settings:
  language: "zh-CN"
  mode: "translate"
CONFIG_YAML

# ---------- systemd service ----------
cat > "$DEPLOY_DIR/orderly-telebot.service" << SYSTEMD_SERVICE
[Unit]
Description=Orderly Telegram Translation Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$DEPLOY_DIR
ExecStart=$DEPLOY_DIR/venv/bin/python3 $DEPLOY_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SYSTEMD_SERVICE

echo -e "${GREEN}✅ 程序文件写入完成${NC}"

# ── 5. 填写密钥并启动 ────────────────────────────────────────
echo ""
echo -e "${YELLOW}[5/5] 填写密钥配置...${NC}"
echo ""

# 读取 Bot Token
while true; do
    read -p "  请输入 Telegram Bot Token: " BOT_TOKEN
    if [ -n "$BOT_TOKEN" ]; then
        break
    fi
    echo -e "  ${RED}❌ Bot Token 不能为空，请重新输入${NC}"
done

# 读取 Gemini API Key
while true; do
    read -p "  请输入 Google Gemini API Key: " GEMINI_KEY
    if [ -n "$GEMINI_KEY" ]; then
        break
    fi
    echo -e "  ${RED}❌ Gemini API Key 不能为空，请重新输入${NC}"
done

# 写入 config.yaml
sed -i "s|REPLACE_WITH_BOT_TOKEN|$BOT_TOKEN|g" "$DEPLOY_DIR/config.yaml"
sed -i "s|REPLACE_WITH_GEMINI_API_KEY|$GEMINI_KEY|g" "$DEPLOY_DIR/config.yaml"

echo ""
echo -e "${GREEN}✅ 密钥已写入 config.yaml${NC}"

# ── 询问启动方式 ─────────────────────────────────────────────
echo ""
echo -e "${BLUE}选择启动方式：${NC}"
echo "  1) screen（推荐，可随时查看日志）"
echo "  2) systemd（开机自启，后台运行）"
echo "  3) 暂不启动"
read -p "请输入选项 [1/2/3]: " START_CHOICE

case "$START_CHOICE" in
    1)
        screen -dmS orderly-telebot bash -c "cd $DEPLOY_DIR && source venv/bin/activate && python3 main.py"
        echo ""
        echo -e "${GREEN}✅ 机器人已在 screen 会话中启动！${NC}"
        echo ""
        echo -e "  查看日志：  ${YELLOW}screen -r orderly-telebot${NC}"
        echo -e "  退出查看：  ${YELLOW}Ctrl+A 然后 D${NC}"
        echo -e "  实时日志：  ${YELLOW}tail -f $DEPLOY_DIR/bot.log${NC}"
        echo -e "  停止机器人：${YELLOW}screen -S orderly-telebot -X quit${NC}"
        ;;
    2)
        sudo cp "$DEPLOY_DIR/orderly-telebot.service" /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable orderly-telebot
        sudo systemctl start orderly-telebot
        sleep 2
        STATUS=$(sudo systemctl is-active orderly-telebot)
        if [ "$STATUS" = "active" ]; then
            echo ""
            echo -e "${GREEN}✅ systemd 服务已启动并设置为开机自启！${NC}"
        else
            echo -e "${RED}❌ 服务启动失败，请查看日志：sudo journalctl -u orderly-telebot -f${NC}"
        fi
        echo ""
        echo -e "  查看状态：  ${YELLOW}sudo systemctl status orderly-telebot${NC}"
        echo -e "  实时日志：  ${YELLOW}sudo journalctl -u orderly-telebot -f${NC}"
        echo -e "  停止服务：  ${YELLOW}sudo systemctl stop orderly-telebot${NC}"
        ;;
    3)
        echo ""
        echo -e "${YELLOW}跳过启动。手动启动方式：${NC}"
        echo -e "  ${YELLOW}cd $DEPLOY_DIR && source venv/bin/activate && python3 main.py${NC}"
        ;;
    *)
        echo -e "${RED}无效选项，跳过启动${NC}"
        ;;
esac

echo ""
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${GREEN}  🎉 部署完成！${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo ""
echo -e "  部署目录：${YELLOW}$DEPLOY_DIR${NC}"
echo -e "  配置文件：${YELLOW}$DEPLOY_DIR/config.yaml${NC}"
echo -e "  运行日志：${YELLOW}$DEPLOY_DIR/bot.log${NC}"
echo ""
echo -e "  如需修改监听的 Topic 或目标群组，编辑 config.yaml 后重启机器人即可。"
echo ""
