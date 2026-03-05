#!/usr/bin/env python3
"""
获取 Twitter OAuth 2.0 初始 Token
这个脚本只需要运行一次，用于获取 access_token 和 refresh_token
"""

import tweepy
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取凭证
CLIENT_ID = os.getenv('X_CLIENT_ID')
CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')
REDIRECT_URI = os.getenv('X_REDIRECT_URI', 'http://localhost:8080/callback')

# 定义所需的权限范围
SCOPES = ["tweet.read", "tweet.write", "users.read", "offline.access"]

def main():
    """主函数：获取初始 OAuth 2.0 token"""
    
    print("=" * 60)
    print("Twitter OAuth 2.0 Token 获取工具")
    print("=" * 60)
    print()
    
    # 验证必需的凭证
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ 错误：缺少必需的环境变量")
        print()
        print("请在 .env 文件中设置：")
        print("  X_CLIENT_ID=你的_client_id")
        print("  X_CLIENT_SECRET=你的_client_secret")
        print("  X_REDIRECT_URI=http://localhost:8080/callback  # 可选")
        print()
        return
    
    print(f"✅ Client ID: {CLIENT_ID[:10]}...")
    print(f"✅ Redirect URI: {REDIRECT_URI}")
    print()
    
    # 创建 OAuth2 处理器
    try:
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            scope=SCOPES,
            client_secret=CLIENT_SECRET
        )
        
        # 生成授权 URL
        auth_url = oauth2_handler.get_authorization_url()
        
        print("📋 步骤 1：访问以下 URL 进行授权")
        print("-" * 60)
        print(auth_url)
        print("-" * 60)
        print()
        print("📋 步骤 2：授权后，浏览器会重定向到一个类似这样的 URL：")
        print(f"  {REDIRECT_URI}?state=...&code=...")
        print()
        print("📋 步骤 3：复制完整的重定向 URL 并粘贴到下面")
        print()
        
        # 获取用户输入的重定向 URL
        response_url = input("请输入授权后的完整 URL: ").strip()
        
        if not response_url:
            print("❌ 错误：未输入 URL")
            return
        
        print()
        print("🔄 正在获取 token...")
        
        # 使用授权码交换 token
        token = oauth2_handler.fetch_token(response_url)
        
        print("✅ Token 获取成功！")
        print()
        print("Token 信息：")
        print(f"  Access Token: {token.get('access_token', '')[:20]}...")
        print(f"  Refresh Token: {token.get('refresh_token', '')[:20]}...")
        print(f"  Expires In: {token.get('expires_in', 'N/A')} 秒")
        print()
        
        # 保存 token 到文件
        token_file = Path(__file__).parent / 'token.json'
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
        
        print(f"✅ Token 已保存到: {token_file}")
        print()
        print("=" * 60)
        print("🎉 设置完成！")
        print("=" * 60)
        print()
        print("下一步：")
        print("  1. 运行 python3 test_oauth.py 测试连接")
        print("  2. 运行 python3 orderly_rub_heat_bot.py 执行主任务")
        print()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        print()
        print("常见问题：")
        print("  - 确保 Redirect URI 在 X Developer Portal 中正确配置")
        print("  - 确保 CLIENT_ID 和 CLIENT_SECRET 正确")
        print("  - 检查授权 URL 是否完整复制")
        

if __name__ == "__main__":
    main()
