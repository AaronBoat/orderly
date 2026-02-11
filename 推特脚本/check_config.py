#!/usr/bin/env python3
"""
配置验证脚本 - 检查所有必需的配置是否正确
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def check_env_vars():
    """检查环境变量"""
    print("🔍 检查环境变量...")
    
    required_vars = {
        'X_API_KEY': os.getenv('X_API_KEY'),
        'X_API_SECRET': os.getenv('X_API_SECRET'),
        'X_ACCESS_TOKEN': os.getenv('X_ACCESS_TOKEN'),
        'X_ACCESS_SECRET': os.getenv('X_ACCESS_SECRET'),
        'X_BEARER_TOKEN': os.getenv('X_BEARER_TOKEN')
    }
    
    optional_vars = {
        'TELEGRAM_TOKEN': os.getenv('TELEGRAM_TOKEN'),
        'TELEGRAM_GROUP_ID': os.getenv('TELEGRAM_GROUP_ID')
    }
    
    missing = []
    for key, value in required_vars.items():
        if not value:
            print(f"  ❌ {key}: 未设置")
            missing.append(key)
        else:
            # 只显示前几个字符
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"  ✅ {key}: {masked}")
    
    print("\n📱 可选配置（Telegram）:")
    for key, value in optional_vars.items():
        if not value:
            print(f"  ⚠️  {key}: 未设置（将不发送 Telegram 报告）")
        else:
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"  ✅ {key}: {masked}")
    
    return len(missing) == 0


def check_materials():
    """检查素材库"""
    print("\n📚 检查素材库...")
    
    materials_file = Path(__file__).parent / 'materials.json'
    
    if not materials_file.exists():
        print(f"  ❌ materials.json 不存在")
        return False
    
    try:
        with open(materials_file, 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        required_keys = ['rwa_snippets', 'trading_snippets', 'templates', 'our_accounts', 'our_post_links']
        missing_keys = [key for key in required_keys if key not in materials]
        
        if missing_keys:
            print(f"  ❌ 缺少必需的字段: {', '.join(missing_keys)}")
            return False
        
        print(f"  ✅ RWA 文案: {len(materials['rwa_snippets'])} 条")
        print(f"  ✅ 交易文案: {len(materials['trading_snippets'])} 条")
        print(f"  ✅ 回复模板: {len(materials['templates'])} 个")
        print(f"  ✅ 账号列表: {', '.join(materials['our_accounts'])}")
        
        # 检查链接是否为示例
        example_links = [link for link in materials['our_post_links'] if 'EXAMPLE' in link]
        if example_links:
            print(f"  ⚠️  警告: {len(example_links)} 个链接仍为示例，请更新为实际链接")
            print(f"     示例: {example_links[0]}")
        else:
            print(f"  ✅ 推文链接: {len(materials['our_post_links'])} 个")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON 格式错误: {e}")
        return False


def check_twitter_connection():
    """检查 Twitter API 连接"""
    print("\n🐦 检查 Twitter API 连接...")
    
    try:
        import tweepy
        
        api_key = os.getenv('X_API_KEY')
        api_secret = os.getenv('X_API_SECRET')
        access_token = os.getenv('X_ACCESS_TOKEN')
        access_secret = os.getenv('X_ACCESS_SECRET')
        bearer_token = os.getenv('X_BEARER_TOKEN')
        
        if not all([api_key, api_secret, access_token, access_secret, bearer_token]):
            print("  ❌ 缺少必需的 API 凭证")
            return False
        
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # 尝试获取自己的用户信息
        me = client.get_me()
        if me.data:
            print(f"  ✅ 连接成功！当前账号: @{me.data.username}")
            return True
        else:
            print("  ❌ 无法获取账号信息")
            return False
            
    except ImportError:
        print("  ❌ 未安装 tweepy，请运行: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"  ❌ 连接失败: {e}")
        return False


def check_telegram():
    """检查 Telegram 配置"""
    print("\n📱 检查 Telegram 配置...")
    
    token = os.getenv('TELEGRAM_TOKEN')
    group_id = os.getenv('TELEGRAM_GROUP_ID')
    
    if not token or not group_id:
        print("  ⚠️  Telegram 未配置（可选功能）")
        return True
    
    try:
        from telegram import Bot
        
        bot = Bot(token=token)
        bot_info = bot.get_me()
        print(f"  ✅ Bot 连接成功: @{bot_info.username}")
        
        # 尝试发送测试消息
        try:
            bot.send_message(
                chat_id=group_id,
                text="🔧 配置验证成功！Orderly 推特机器人已准备就绪。"
            )
            print(f"  ✅ 测试消息已发送到群组")
        except Exception as e:
            print(f"  ⚠️  无法发送消息到群组: {e}")
            print(f"     请确认 Bot 已加入群组且有发送消息权限")
        
        return True
        
    except ImportError:
        print("  ❌ 未安装 python-telegram-bot，请运行: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"  ❌ Telegram 配置错误: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🛠️  Orderly 推特机器人 - 配置验证")
    print("=" * 60)
    print()
    
    # 检查 .env 文件
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("❌ 未找到 .env 文件")
        print("\n请按以下步骤操作：")
        print("  1. cp .env.example .env")
        print("  2. 编辑 .env 文件，填入你的 API 凭证")
        print("  3. 重新运行此验证脚本")
        return
    
    results = []
    
    # 执行各项检查
    results.append(("环境变量", check_env_vars()))
    results.append(("素材库", check_materials()))
    results.append(("Twitter API", check_twitter_connection()))
    results.append(("Telegram", check_telegram()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证结果总结")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有配置验证通过！可以运行机器人了。")
        print("\n运行命令:")
        print("  ./run_bot.sh")
        print("或")
        print("  python3 orderly_rub_heat_bot.py")
    else:
        print("⚠️  部分配置未通过验证，请修复后再运行机器人。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
