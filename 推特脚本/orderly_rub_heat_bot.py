#!/usr/bin/env python3
"""
Orderly 推特"蹭热点"自动化脚本
每日自动搜索热门推文，生成回复并发送到 Telegram 群聊报告
"""

import tweepy
import json
import random
import time
import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orderly_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 从环境变量加载凭证
API_KEY = os.getenv('X_API_KEY')
API_SECRET = os.getenv('X_API_SECRET')
ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('X_ACCESS_SECRET')
BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')

# 配置文件路径
MATERIALS_FILE = Path(__file__).parent / 'materials.json'
REPLIED_POSTS_FILE = Path(__file__).parent / 'replied_posts.json'


class OrderlyRubHeatBot:
    """Orderly 推特蹭热点机器人"""
    
    def __init__(self):
        """初始化机器人"""
        self.validate_credentials()
        self.client = self.authenticate_twitter()
        self.materials = self.load_materials()
        self.replied_posts = self.load_replied_posts()
        
    def validate_credentials(self):
        """验证必需的凭证是否存在"""
        required = {
            'X_API_KEY': API_KEY,
            'X_API_SECRET': API_SECRET,
            'X_ACCESS_TOKEN': ACCESS_TOKEN,
            'X_ACCESS_SECRET': ACCESS_SECRET,
            'X_BEARER_TOKEN': BEARER_TOKEN
        }
        
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"缺少必需的环境变量: {', '.join(missing)}")
    
    def authenticate_twitter(self):
        """认证 Twitter API"""
        try:
            client = tweepy.Client(
                bearer_token=BEARER_TOKEN,
                consumer_key=API_KEY,
                consumer_secret=API_SECRET,
                access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_SECRET,
                wait_on_rate_limit=True
            )
            logger.info("Twitter API 认证成功")
            return client
        except Exception as e:
            logger.error(f"Twitter API 认证失败: {e}")
            raise
    
    def load_materials(self):
        """加载素材库"""
        try:
            with open(MATERIALS_FILE, 'r', encoding='utf-8') as f:
                materials = json.load(f)
            logger.info("素材库加载成功")
            return materials
        except FileNotFoundError:
            logger.error(f"素材库文件不存在: {MATERIALS_FILE}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"素材库 JSON 格式错误: {e}")
            raise
    
    def load_replied_posts(self):
        """加载已回复的推文ID"""
        if REPLIED_POSTS_FILE.exists():
            try:
                with open(REPLIED_POSTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("replied_posts.json 格式错误，重新创建")
                return []
        return []
    
    def save_replied_posts(self):
        """保存已回复的推文ID"""
        # 只保留最近 100 条，避免文件过大
        self.replied_posts = self.replied_posts[-100:]
        with open(REPLIED_POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.replied_posts, f, indent=2)
    
    def search_hot_posts(self, max_results=50):
        """搜索热门推文"""
        query = (
            '(AI OR RWA OR "real world assets" OR trading OR DEX OR '
            '"decentralized exchange" OR rally OR market OR crypto) '
            'lang:en -is:retweet -from:OrderlyCN_ -from:OrderlyNetwork'
        )
        
        try:
            logger.info(f"开始搜索热门推文: {query}")
            response = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                max_results=max_results
            )
            
            if not response.data:
                logger.warning("未找到符合条件的推文")
                return []
            
            # 过滤并排序
            now = datetime.now(response.data[0].created_at.tzinfo)
            candidates = []
            
            for tweet in response.data:
                # 跳过已回复的
                if tweet.id in self.replied_posts:
                    continue
                
                # 检查时间和互动数
                age_days = (now - tweet.created_at).days
                likes = tweet.public_metrics['like_count']
                
                if age_days < 3 and likes > 50:
                    candidates.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'likes': likes,
                        'retweets': tweet.public_metrics['retweet_count'],
                        'replies': tweet.public_metrics['reply_count'],
                        'age_days': age_days
                    })
            
            # 按点赞数排序
            candidates.sort(key=lambda x: x['likes'], reverse=True)
            logger.info(f"找到 {len(candidates)} 个候选推文")
            return candidates[:5]
            
        except tweepy.TweepyException as e:
            logger.error(f"搜索推文失败: {e}")
            return []
    
    def detect_topic(self, text):
        """检测推文主题"""
        text_upper = text.upper()
        
        if 'RWA' in text_upper or 'REAL WORLD ASSET' in text_upper:
            return 'rwa'
        elif 'AI' in text_upper or 'ARTIFICIAL INTELLIGENCE' in text_upper:
            return 'ai'
        elif 'DEX' in text_upper or 'DECENTRALIZED' in text_upper:
            return 'dex'
        elif 'TRADING' in text_upper or 'TRADE' in text_upper:
            return 'trading'
        else:
            return 'general'
    
    def generate_reply(self, post):
        """生成回复内容"""
        topic = self.detect_topic(post['text'])
        
        # 选择模板和素材
        template = random.choice(self.materials['templates'])
        
        # 根据主题选择素材片段
        if topic == 'rwa':
            snippet = random.choice(self.materials['rwa_snippets'])
        elif topic in ['trading', 'dex']:
            snippet = random.choice(self.materials['trading_snippets'])
        else:
            snippet = random.choice(
                self.materials['rwa_snippets'] + self.materials['trading_snippets']
            )
        
        # 选择账号和链接
        our_account = random.choice(self.materials['our_accounts'])
        our_link = random.choice(self.materials['our_post_links'])
        
        # 添加变化前缀
        variations = [
            'Great point!', 'Totally agree!', 'This is key!', 
            'Interesting perspective!', 'Spot on!', 'Well said!'
        ]
        prefix = random.choice(variations)
        
        # 构建回复
        topic_name = {
            'rwa': 'RWA',
            'ai': 'AI in trading',
            'dex': 'DEX trading',
            'trading': 'market trends',
            'general': 'crypto'
        }.get(topic, 'crypto')
        
        reply_text = template.format(
            topic=topic_name,
            snippet=snippet,
            our_post_link=our_link,
            our_account=our_account
        )
        
        # 添加一些自然变化
        reply_text = reply_text.replace('interesting', random.choice(['fascinating', 'compelling', 'intriguing']))
        
        return f"{prefix} {reply_text}"
    
    def post_reply(self, post_id, reply_text):
        """发布回复"""
        try:
            response = self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=post_id
            )
            logger.info(f"成功回复推文 {post_id}")
            return response.data['id']
        except tweepy.TweepyException as e:
            logger.error(f"回复推文失败: {e}")
            return None
    
    def send_telegram_report(self, summary):
        """发送 Telegram 报告"""
        if not TELEGRAM_TOKEN or not TELEGRAM_GROUP_ID:
            logger.warning("未配置 Telegram，跳过发送报告")
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=TELEGRAM_TOKEN)
            
            message = "🔥 Orderly 今日蹭热点报告 🔥\n\n" + "\n\n".join(summary)
            bot.send_message(chat_id=TELEGRAM_GROUP_ID, text=message, parse_mode='Markdown')
            logger.info("Telegram 报告发送成功")
        except Exception as e:
            logger.error(f"Telegram 报告发送失败: {e}")
    
    def run_daily_task(self):
        """执行每日任务"""
        logger.info("=" * 60)
        logger.info(f"开始执行每日任务 - {datetime.now()}")
        logger.info("=" * 60)
        
        # 搜索热门推文
        hot_posts = self.search_hot_posts()
        
        if not hot_posts:
            logger.warning("未找到足够的热门推文，任务结束")
            return
        
        summary = []
        success_count = 0
        
        # 对每个推文生成并发布回复
        for i, post in enumerate(hot_posts, 1):
            logger.info(f"\n处理推文 {i}/5: {post['id']}")
            logger.info(f"推文内容: {post['text'][:100]}...")
            logger.info(f"互动数据: {post['likes']} 赞, {post['retweets']} 转发")
            
            # 生成回复
            reply_text = self.generate_reply(post)
            logger.info(f"生成回复: {reply_text[:100]}...")
            
            # 发布回复
            reply_id = self.post_reply(post['id'], reply_text)
            
            if reply_id:
                success_count += 1
                self.replied_posts.append(post['id'])
                
                summary.append(
                    f"✅ 推文 {i}\n"
                    f"原文: https://x.com/status/{post['id']}\n"
                    f"回复: https://x.com/status/{reply_id}\n"
                    f"内容: {reply_text[:80]}..."
                )
                
                # 等待避免速率限制
                if i < len(hot_posts):
                    wait_time = random.randint(30, 90)
                    logger.info(f"等待 {wait_time} 秒...")
                    time.sleep(wait_time)
            else:
                summary.append(
                    f"❌ 推文 {i}\n"
                    f"原文: https://x.com/status/{post['id']}\n"
                    f"状态: 回复失败"
                )
        
        # 保存已回复记录
        self.save_replied_posts()
        
        # 发送报告
        summary_header = [f"📊 成功回复: {success_count}/5\n"]
        self.send_telegram_report(summary_header + summary)
        
        logger.info("=" * 60)
        logger.info(f"任务完成！成功回复 {success_count} 条")
        logger.info("=" * 60)


def main():
    """主函数"""
    try:
        bot = OrderlyRubHeatBot()
        bot.run_daily_task()
    except Exception as e:
        logger.error(f"程序执行出错: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
