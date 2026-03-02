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

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 消息去重队列（最近 50 条消息 ID）
recent_message_ids = deque(maxlen=50)

# 翻译 Prompt
TRANSLATION_PROMPT = """你是一个专业的翻译官。请将输入的 Telegram 消息翻译成中文。要求：保持原有的 Emoji 位置，保留专有名词（如项目名、代码），语言风格要自然、符合中文社交媒体习惯。仅返回翻译后的文本，不要有任何解释说明。"""


class Config:
    """配置管理类"""
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.bot_token = config['telegram']['bot_token']
        self.source_chat_id = int(config['telegram']['source_chat_id'])
        self.target_chat_id = int(config['telegram']['target_chat_id'])
        
        # 允许的 Topic 名称或 ID（可选）
        self.allowed_topics = config['telegram'].get('allowed_topics', [])
        # 转换为小写以便不区分大小写匹配
        self.allowed_topics_lower = [str(t).lower() for t in self.allowed_topics] if self.allowed_topics else []
        
        self.gemini_api_key = config['gemini']['api_key']
        self.gemini_model = config['gemini']['model_name']
        self.language = config['settings']['language']


class GeminiTranslator:
    """Gemini API 翻译器"""
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.max_retries = 3
    
    async def translate(self, text: str) -> Optional[str]:
        """
        翻译文本，支持重试机制
        
        Args:
            text: 待翻译的文本
            
        Returns:
            翻译后的文本，失败返回 None
        """
        for attempt in range(self.max_retries):
            try:
                # 构建完整的 prompt
                full_prompt = f"{TRANSLATION_PROMPT}\n\n原文：\n{text}"
                
                # 调用 Gemini API
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    full_prompt
                )
                
                translated_text = response.text.strip()
                logger.info(f"翻译成功 (尝试 {attempt + 1}/{self.max_retries})")
                return translated_text
                
            except Exception as e:
                logger.error(f"翻译失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    # 指数退避
                    wait_time = 2 ** attempt
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("翻译失败，已达到最大重试次数")
                    return None


class TranslationBot:
    """Telegram 翻译转发机器人"""
    def __init__(self, config: Config):
        self.config = config
        self.translator = GeminiTranslator(
            config.gemini_api_key,
            config.gemini_model
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        处理接收到的消息
        
        Args:
            update: Telegram 更新对象
            context: 上下文对象
        """
        message = update.message or update.channel_post
        
        if not message:
            return
        
        # 检查消息来源
        if message.chat_id != self.config.source_chat_id:
            logger.debug(f"忽略非源群组消息: {message.chat_id}")
            return
        
        # 检查是否来自允许的 Topic（如果配置了 allowed_topics）
        if self.config.allowed_topics_lower:
            topic_id = message.message_thread_id
            topic_name = None
            
            # 尝试获取 Topic 名称
            if topic_id:
                try:
                    forum_topic = await context.bot.get_forum_topic_icon_custom_emoji_stickers(
                        chat_id=message.chat_id
                    )
                    # 注意：实际的 Topic 名称获取可能需要不同的方法
                    # 这里我们主要通过 message_thread_id 来判断
                except:
                    pass
            
            # 如果设置了 allowed_topics，检查是否匹配
            # 可以通过 Topic ID 或从消息中获取的信息来判断
            should_process = False
            
            if topic_id:
                # 如果配置中包含数字（Topic ID），进行匹配
                if str(topic_id) in [str(t) for t in self.config.allowed_topics]:
                    should_process = True
                    logger.info(f"消息来自允许的 Topic ID: {topic_id}")
            
            # 由于无法直接获取 Topic 名称，我们记录 Topic ID 供用户参考
            if not should_process and topic_id:
                logger.info(f"消息来自 Topic ID: {topic_id}，但不在允许列表中，跳过")
                logger.info(f"如需监听此 Topic，请在 config.yaml 的 allowed_topics 中添加: {topic_id}")
                return
            elif not should_process and not topic_id:
                logger.info(f"消息不在任何 Topic 中，且配置了 Topic 过滤，跳过")
                return
        
        # 去重检查
        if message.message_id in recent_message_ids:
            logger.info(f"消息 {message.message_id} 已处理，跳过")
            return
        
        recent_message_ids.append(message.message_id)
        
        logger.info(f"收到新消息 ID: {message.message_id} from Chat: {message.chat_id}")
        
        # 提取文本内容
        text_to_translate = None
        has_media = False
        
        if message.text:
            text_to_translate = message.text
        elif message.caption:
            text_to_translate = message.caption
            has_media = True
        
        # 如果没有文本且没有媒体，跳过
        if not text_to_translate and not (message.photo or message.video or message.document):
            logger.info("消息无内容，跳过")
            return
        
        # 如果只有媒体没有文本，直接转发
        if not text_to_translate:
            logger.info("消息无文本内容，直接转发媒体")
            await self._forward_message(message, context)
            return
        
        # 翻译文本
        translated_text = await self.translator.translate(text_to_translate)
        
        if not translated_text:
            logger.error("翻译失败，转发原消息")
            await self._forward_message(message, context)
            return
        
        # 发送翻译后的消息
        await self._send_translated_message(message, translated_text, context)
    
    async def _forward_message(self, message, context: ContextTypes.DEFAULT_TYPE):
        """
        直接转发消息（用于无文本或翻译失败的情况）
        
        Args:
            message: 原始消息对象
            context: 上下文对象
        """
        try:
            # 尝试不同的转发方式
            if message.photo:
                photo = message.photo[-1]
                await context.bot.send_photo(
                    chat_id=self.config.target_chat_id,
                    photo=photo.file_id,
                    caption=message.caption or ""
                )
            elif message.video:
                await context.bot.send_video(
                    chat_id=self.config.target_chat_id,
                    video=message.video.file_id,
                    caption=message.caption or ""
                )
            elif message.document:
                await context.bot.send_document(
                    chat_id=self.config.target_chat_id,
                    document=message.document.file_id,
                    caption=message.caption or ""
                )
            elif message.text:
                await context.bot.send_message(
                    chat_id=self.config.target_chat_id,
                    text=message.text
                )
            else:
                # 如果都不是，记录跳过
                logger.info(f"消息 {message.message_id} 类型不支持，跳过")
                return
                
            logger.info(f"消息 {message.message_id} 已直接转发")
        except Exception as e:
            logger.error(f"转发消息失败: {e}")
    
    async def _send_translated_message(
        self,
        message,
        translated_text: str,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        发送翻译后的消息，保留格式
        
        Args:
            message: 原始消息对象
            translated_text: 翻译后的文本
            context: 上下文对象
        """
        try:
            # 处理长文本拆分（Telegram 限制 4096 字符）
            max_length = 4000  # 留一些余量
            text_chunks = self._split_text(translated_text, max_length)
            
            # 如果有图片，发送图片并附带翻译文本
            if message.photo:
                # 获取最高质量的图片
                photo = message.photo[-1]
                
                # 发送第一段文本作为 caption
                await context.bot.send_photo(
                    chat_id=self.config.target_chat_id,
                    photo=photo.file_id,
                    caption=text_chunks[0] if text_chunks else translated_text,
                    parse_mode='Markdown'
                )
                
                # 如果有多段，继续发送剩余文本
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)  # 避免触发速率限制
                    await context.bot.send_message(
                        chat_id=self.config.target_chat_id,
                        text=chunk,
                        parse_mode='Markdown'
                    )
            
            # 如果有视频
            elif message.video:
                await context.bot.send_video(
                    chat_id=self.config.target_chat_id,
                    video=message.video.file_id,
                    caption=text_chunks[0] if text_chunks else translated_text,
                    parse_mode='Markdown'
                )
                
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)
                    await context.bot.send_message(
                        chat_id=self.config.target_chat_id,
                        text=chunk,
                        parse_mode='Markdown'
                    )
            
            # 如果有文档
            elif message.document:
                await context.bot.send_document(
                    chat_id=self.config.target_chat_id,
                    document=message.document.file_id,
                    caption=text_chunks[0] if text_chunks else translated_text,
                    parse_mode='Markdown'
                )
                
                for chunk in text_chunks[1:]:
                    await asyncio.sleep(0.5)
                    await context.bot.send_message(
                        chat_id=self.config.target_chat_id,
                        text=chunk,
                        parse_mode='Markdown'
                    )
            
            # 纯文本消息
            else:
                for chunk in text_chunks:
                    await context.bot.send_message(
                        chat_id=self.config.target_chat_id,
                        text=chunk,
                        parse_mode='Markdown'
                    )
                    if len(text_chunks) > 1:
                        await asyncio.sleep(0.5)
            
            logger.info(f"消息 {message.message_id} 翻译转发成功")
            
        except Exception as e:
            logger.error(f"发送翻译消息失败: {e}")
            # 尝试直接转发原消息
            await self._forward_message(message, context)
    
    @staticmethod
    def _split_text(text: str, max_length: int) -> list[str]:
        """
        将长文本拆分为多个片段
        
        Args:
            text: 原始文本
            max_length: 每段的最大长度
            
        Returns:
            文本片段列表
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # 按行拆分
        lines = text.split('\n')
        
        for line in lines:
            # 如果单行就超过限制，强制拆分
            if len(line) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # 强制按字符拆分
                for i in range(0, len(line), max_length):
                    chunks.append(line[i:i + max_length])
            
            # 如果添加这行会超过限制，先保存当前块
            elif len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            
            else:
                current_chunk += line + '\n'
        
        # 添加最后一块
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """处理错误"""
    logger.error(f"更新 {update} 引发错误：{context.error}")


def main():
    """主函数"""
    try:
        # 加载配置
        config = Config()
        logger.info("配置加载成功")
        
        # 创建机器人实例
        bot = TranslationBot(config)
        
        # 创建 Application
        application = Application.builder().token(config.bot_token).build()
        
        # 添加消息处理器（处理文本和图片）
        application.add_handler(
            MessageHandler(
                filters.ChatType.GROUPS | filters.ChatType.CHANNEL,
                bot.handle_message
            )
        )
        
        # 添加错误处理器
        application.add_error_handler(error_handler)
        
        # 启动机器人
        logger.info("机器人启动中...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except FileNotFoundError:
        logger.error("配置文件 config.yaml 不存在，请先创建配置文件")
    except Exception as e:
        logger.error(f"启动失败: {e}")


if __name__ == "__main__":
    main()
