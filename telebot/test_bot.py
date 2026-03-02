#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot 配置和连接测试脚本
在启动完整 Bot 之前，先测试配置是否正确
"""

import sys
import asyncio
import yaml
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("❌ 错误：config.yaml 不存在")
        print("请先运行: cp config.yaml.example config.yaml")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("✅ 配置文件加载成功")
        return config
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return None

def check_config(config):
    """检查配置项"""
    print("\n" + "="*50)
    print("📋 配置检查")
    print("="*50)
    
    issues = []
    
    # 检查 Telegram 配置
    bot_token = config['telegram']['bot_token']
    if bot_token == "YOUR_BOT_TOKEN" or not bot_token:
        print("❌ Bot Token 未设置")
        issues.append("Bot Token")
    else:
        masked_token = bot_token[:10] + "..." + bot_token[-10:]
        print(f"✅ Bot Token: {masked_token}")
    
    source_id = config['telegram']['source_chat_id']
    if source_id == -100000000 or str(source_id) == "-100xxxxxx":
        print("❌ 源群组 ID 未设置")
        issues.append("源群组 ID")
    else:
        print(f"✅ 源群组 ID: {source_id}")
    
    target_id = config['telegram']['target_chat_id']
    if target_id == -100000000 or str(target_id) == "-100xxxxxx":
        print("❌ 目标群组 ID 未设置")
        issues.append("目标群组 ID")
    else:
        print(f"✅ 目标群组 ID: {target_id}")
    
    # 检查 Gemini 配置
    api_key = config['gemini']['api_key']
    if api_key == "YOUR_GEMINI_API_KEY" or not api_key:
        print("❌ Gemini API Key 未设置")
        issues.append("Gemini API Key")
    else:
        masked_key = api_key[:10] + "..." + api_key[-10:]
        print(f"✅ Gemini API Key: {masked_key}")
    
    model = config['gemini']['model_name']
    print(f"✅ Gemini 模型: {model}")
    
    return len(issues) == 0, issues

async def test_telegram_connection(config):
    """测试 Telegram Bot 连接"""
    print("\n" + "="*50)
    print("🤖 测试 Telegram Bot 连接")
    print("="*50)
    
    try:
        from telegram import Bot
        
        bot = Bot(token=config['telegram']['bot_token'])
        me = await bot.get_me()
        
        print(f"✅ Bot 连接成功！")
        print(f"   Bot 用户名: @{me.username}")
        print(f"   Bot 名称: {me.first_name}")
        print(f"   Bot ID: {me.id}")
        
        return True
    except Exception as e:
        print(f"❌ Bot 连接失败: {e}")
        return False

async def test_gemini_connection(config):
    """测试 Gemini API 连接"""
    print("\n" + "="*50)
    print("🤖 测试 Gemini API 连接")
    print("="*50)
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=config['gemini']['api_key'])
        model = genai.GenerativeModel(config['gemini']['model_name'])
        
        # 简单测试
        response = await asyncio.to_thread(
            model.generate_content,
            "Say 'Hello' in one word"
        )
        
        print(f"✅ Gemini API 连接成功！")
        print(f"   模型: {config['gemini']['model_name']}")
        print(f"   测试响应: {response.text.strip()}")
        
        return True
    except Exception as e:
        print(f"❌ Gemini API 连接失败: {e}")
        return False

async def test_chat_access(config):
    """测试群组访问权限"""
    print("\n" + "="*50)
    print("👥 测试群组访问权限")
    print("="*50)
    
    try:
        from telegram import Bot
        
        bot = Bot(token=config['telegram']['bot_token'])
        
        # 测试源群组
        try:
            source_chat = await bot.get_chat(config['telegram']['source_chat_id'])
            print(f"✅ 源群组访问成功")
            print(f"   名称: {source_chat.title}")
            print(f"   类型: {source_chat.type}")
        except Exception as e:
            print(f"❌ 源群组访问失败: {e}")
            print("   请确保 Bot 已加入源群组并设为管理员")
        
        # 测试目标群组
        try:
            target_chat = await bot.get_chat(config['telegram']['target_chat_id'])
            print(f"✅ 目标群组访问成功")
            print(f"   名称: {target_chat.title}")
            print(f"   类型: {target_chat.type}")
        except Exception as e:
            print(f"❌ 目标群组访问失败: {e}")
            print("   请确保 Bot 已加入目标群组并设为管理员")
        
        return True
    except Exception as e:
        print(f"❌ 群组测试失败: {e}")
        return False

async def main():
    """主测试流程"""
    print("\n" + "="*50)
    print("  🚀 Telegram Bot 配置测试")
    print("="*50)
    
    # 加载配置
    config = load_config()
    if not config:
        sys.exit(1)
    
    # 检查配置
    config_ok, issues = check_config(config)
    if not config_ok:
        print(f"\n❌ 配置不完整，缺少: {', '.join(issues)}")
        print("请编辑 config.yaml 填入正确的配置")
        sys.exit(1)
    
    # 测试连接
    telegram_ok = await test_telegram_connection(config)
    gemini_ok = await test_gemini_connection(config)
    chat_ok = await test_chat_access(config)
    
    # 总结
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    print(f"配置文件: {'✅' if config_ok else '❌'}")
    print(f"Telegram Bot: {'✅' if telegram_ok else '❌'}")
    print(f"Gemini API: {'✅' if gemini_ok else '❌'}")
    print(f"群组访问: {'✅' if chat_ok else '❌'}")
    
    if telegram_ok and gemini_ok and chat_ok:
        print("\n🎉 所有测试通过！可以启动 Bot 了")
        print("运行: ./start_bot.sh 或 python3 main.py")
    else:
        print("\n⚠️  存在问题，请修复后再启动 Bot")
    
    print("="*50)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n测试被中断")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        sys.exit(1)
