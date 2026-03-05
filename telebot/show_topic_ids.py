#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速显示最近处理的消息及其 Topic ID
"""

import re
import subprocess

print("\n" + "="*60)
print("  📊 查找最近的 Topic ID")
print("="*60 + "\n")

try:
    # 获取 screen 会话中的内容
    result = subprocess.run(
        ["screen", "-S", "telegram-bot", "-X", "hardcopy", "/tmp/screen_log.txt"],
        capture_output=True,
        text=True
    )
    
    # 读取日志
    try:
        with open("/tmp/screen_log.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找 Topic ID
        topic_pattern = r"📌 消息来自 Topic ID: (\d+)"
        matches = re.findall(topic_pattern, content)
        
        if matches:
            print("找到以下 Topic ID：\n")
            unique_topics = list(set(matches))
            for i, topic_id in enumerate(unique_topics, 1):
                print(f"  {i}. Topic ID: {topic_id}")
            
            print("\n" + "="*60)
            print("💡 这些就是你需要的 Topic ID")
            print("="*60 + "\n")
        else:
            print("❌ 未找到 Topic ID")
            print("   可能原因：")
            print("   1. Bot 刚启动，还没收到消息")
            print("   2. 日志已被清空")
            print("\n   请在 Forum 中发送一条测试消息，然后重新运行此脚本")
    except FileNotFoundError:
        print("❌ 无法读取日志文件")
        print("   请运行: screen -r telegram-bot 手动查看日志")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    print("\n🔧 手动查看方法：")
    print("   1. 运行: screen -r telegram-bot")
    print("   2. 查找带有 📌 的行")
    print("   3. 记录 Topic ID")
    print("   4. 按 Ctrl+A 然后 D 退出")
