#!/usr/bin/env python3
"""
简单的配置检查脚本（不需要实际 API 调用）
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def main():
    print()
    print("=" * 60)
    print("🔍 推特脚本配置检查")
    print("=" * 60)
    print()
    
    # 1. 检查环境变量
    print("1️⃣  环境变量配置")
    print("-" * 60)
    
    env_vars = {
        'X_CLIENT_ID': os.getenv('X_CLIENT_ID'),
        'X_CLIENT_SECRET': os.getenv('X_CLIENT_SECRET'),
        'X_BEARER_TOKEN': os.getenv('X_BEARER_TOKEN'),
        'X_REDIRECT_URI': os.getenv('X_REDIRECT_URI', 'http://localhost:8080/callback')
    }
    
    for key, value in env_vars.items():
        if value:
            masked = value[:15] + '...' if len(value) > 15 else value
            print(f"  ✅ {key}: {masked}")
        else:
            print(f"  ❌ {key}: 未设置")
    
    print()
    
    # 2. 检查 token 文件
    print("2️⃣  Token 文件")
    print("-" * 60)
    
    token_file = Path('token.json')
    if token_file.exists():
        try:
            with open(token_file, 'r') as f:
                token = json.load(f)
            print(f"  ✅ token.json 存在")
            print(f"  ✅ Access Token: {token.get('access_token', '')[:20]}...")
            print(f"  ✅ Refresh Token: {token.get('refresh_token', '')[:20]}...")
        except:
            print(f"  ⚠️  token.json 格式错误")
    else:
        print(f"  ℹ️  token.json 不存在（首次使用正常）")
        print(f"  📝 需要运行: python3 get_initial_token.py")
    
    print()
    
    # 3. 检查素材库
    print("3️⃣  素材库")
    print("-" * 60)
    
    materials_file = Path('materials.json')
    if materials_file.exists():
        try:
            with open(materials_file, 'r', encoding='utf-8') as f:
                materials = json.load(f)
            
            print(f"  ✅ materials.json 存在")
            print(f"  📝 RWA 文案: {len(materials.get('rwa_snippets', []))} 条")
            print(f"  📝 交易文案: {len(materials.get('trading_snippets', []))} 条")
            print(f"  📝 回复模板: {len(materials.get('templates', []))} 个")
            
            links = materials.get('our_post_links', [])
            example_count = sum(1 for link in links if 'EXAMPLE' in link)
            if example_count > 0:
                print(f"  ⚠️  还有 {example_count} 个示例链接需要更新")
            else:
                print(f"  ✅ 推文链接: {len(links)} 个（已更新）")
        except:
            print(f"  ❌ materials.json 格式错误")
    else:
        print(f"  ❌ materials.json 不存在")
    
    print()
    
    # 4. 检查依赖
    print("4️⃣  Python 依赖")
    print("-" * 60)
    
    required_packages = ['tweepy', 'dotenv', 'requests']
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} 未安装")
    
    print()
    
    # 总结
    print("=" * 60)
    print("📋 下一步操作")
    print("=" * 60)
    print()
    
    if not token_file.exists():
        print("🔑 首次设置 OAuth 2.0:")
        print()
        print("  1. 运行获取 token:")
        print("     python3 get_initial_token.py")
        print()
        print("  2. 跟随提示完成授权")
        print()
        print("  3. 测试配置:")
        print("     python3 test_oauth.py")
        print()
    else:
        print("✅ 配置完整！")
        print()
        print("📝 更新素材库:")
        print("  编辑 materials.json，更新推文链接")
        print()
        print("🚀 运行脚本:")
        print("  python3 orderly_rub_heat_bot_oauth2.py")
        print()
    
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
