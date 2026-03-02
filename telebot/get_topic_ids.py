#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取 Forum Topic ID 的辅助工具
运行此脚本，然后在 Forum 中发送消息，会显示 Topic ID
"""

import asyncio
import yaml
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

def load_config():
    """加载配置"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

async def show_topic_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """显示消息的 Topic 信息"""
    message = update.message or update.channel_post
    
    if not message:
        return
    
    print("\n" + "="*60)
    print(f"📩 收到消息")
    print("="*60)
    print(f"Chat ID: {message.chat_id}")
    print(f"Message ID: {message.message_id}")
    
    if message.message_thread_id:
        print(f"✅ Topic ID (message_thread_id): {message.message_thread_id}")
        print(f"\n💡 将此 ID 添加到 config.yaml 的 allowed_topics 中：")
        print(f"   allowed_topics:")
        print(f"     - {message.message_thread_id}")
    else:
        print("❌ 此消息不在任何 Topic 中（可能是主群组消息）")
    
    if message.text:
        print(f"文本内容: {message.text[:50]}...")
    elif message.caption:
        print(f"媒体说明: {message.caption[:50]}...")
    
    print("="*60 + "\n")

async def main():
    """主函数"""
    print("\n" + "="*60)
    print("  📡 Forum Topic ID 检测工具")
    print("="*60)
    print("\n正在加载配置...")
    
    try:
        config = load_config()
        bot_token = config['telegram']['bot_token']
        source_chat_id = config['telegram']['source_chat_id']
        
        print(f"✅ Bot Token: {bot_token[:20]}...")
        print(f"✅ 监听群组: {source_chat_id}")
        print("\n" + "="*60)
        print("🎯 Bot 已启动，正在监听...")
        print("💡 在 Forum 的不同 Topic 中发送消息")
        print("💡 每条消息会显示其 Topic ID")
        print("💡 按 Ctrl+C 停止")
        print("="*60 + "\n")
        
        # 创建应用
        application = Application.builder().token(bot_token).build()
        
        # 添加消息处理器
        application.add_handler(
            MessageHandler(
                filters.ChatType.GROUPS | filters.ChatType.CHANNEL | filters.ChatType.SUPERGROUP,
                show_topic_info
            )
        )
        
        # 启动
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except FileNotFoundError:
        print("❌ 错误：config.yaml 不存在")
    except KeyError as e:
        print(f"❌ 配置错误：缺少 {e}")
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 已停止监听")
