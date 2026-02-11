# Orderly 推特"蹭热点"自动化脚本

这是一个自动化脚本，用于每天在 Twitter/X 上搜索热门推文并自动回复，帮助 Orderly 推广品牌内容。

## 功能特性

- 🔍 **智能搜索**：自动搜索 AI、RWA、DEX、交易等相关热门推文
- 🤖 **智能回复**：根据推文主题生成个性化回复，避免垃圾信息
- 📊 **互动筛选**：只选择高互动度（>50 赞）和新鲜度（<3 天）的推文
- 🔄 **去重机制**：记录已回复的推文，避免重复回复
- 📱 **Telegram 报告**：每日执行后自动发送详细报告到群聊
- ⏰ **定时执行**：支持通过 cron 定时任务每日自动运行

## 前置要求

### 1. Twitter/X Developer 账号

1. 访问 [developer.x.com](https://developer.x.com)
2. 创建一个新的 App
3. 启用 OAuth 2.0 认证
4. 获取以下凭证：
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### 2. Telegram Bot（可选）

如果需要接收每日报告：

1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 创建新机器人，获取 Bot Token
3. 将机器人添加到目标群组
4. 获取群组 ID（可使用 [@userinfobot](https://t.me/userinfobot)）

### 3. Python 环境

- Python 3.10 或更高版本
- pip 包管理器

## 安装步骤

### 1. 克隆或下载项目

```bash
cd /Users/aaron/orderly打工/推特脚本
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或者使用虚拟环境（推荐）：

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的凭证：

```bash
# Twitter/X API 凭证
X_API_KEY=你的_api_key
X_API_SECRET=你的_api_secret
X_ACCESS_TOKEN=你的_access_token
X_ACCESS_SECRET=你的_access_secret
X_BEARER_TOKEN=你的_bearer_token

# Telegram Bot 配置（可选）
TELEGRAM_TOKEN=你的_telegram_bot_token
TELEGRAM_GROUP_ID=你的_telegram_group_id
```

### 4. 更新素材库

编辑 `materials.json` 文件：

1. 将 `our_post_links` 中的 `EXAMPLE1`、`EXAMPLE2` 等替换为实际的推文链接
2. 根据需要更新或添加 `rwa_snippets` 和 `trading_snippets` 中的文案
3. 根据需要调整 `templates` 中的回复模板

示例：

```json
{
  "our_post_links": [
    "https://x.com/OrderlyCN_/status/1234567890123456789",
    "https://x.com/OrderlyNetwork/status/9876543210987654321"
  ]
}
```

## 使用方法

### 手动运行（测试）

在配置完成后，可以先手动运行测试：

```bash
# 加载环境变量并运行
source .env  # macOS/Linux
python3 orderly_rub_heat_bot.py
```

或者使用 python-dotenv 自动加载（脚本已内置）：

```bash
python3 orderly_rub_heat_bot.py
```

### 自动化运行（生产环境）

#### 方法 1：使用 cron（macOS/Linux）

1. 打开 crontab 编辑器：

```bash
crontab -e
```

2. 添加定时任务（每天上午 10:00 运行）：

```bash
0 10 * * * cd /Users/aaron/orderly打工/推特脚本 && /usr/bin/python3 orderly_rub_heat_bot.py >> /Users/aaron/orderly打工/推特脚本/cron.log 2>&1
```

或者使用虚拟环境：

```bash
0 10 * * * cd /Users/aaron/orderly打工/推特脚本 && /Users/aaron/orderly打工/推特脚本/venv/bin/python orderly_rub_heat_bot.py >> /Users/aaron/orderly打工/推特脚本/cron.log 2>&1
```

3. 保存并退出

#### 方法 2：使用 launchd（macOS）

创建 `~/Library/LaunchAgents/com.orderly.rubheat.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.orderly.rubheat</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/aaron/orderly打工/推特脚本/orderly_rub_heat_bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/aaron/orderly打工/推特脚本</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/aaron/orderly打工/推特脚本/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/aaron/orderly打工/推特脚本/launchd.err</string>
</dict>
</plist>
```

加载任务：

```bash
launchctl load ~/Library/LaunchAgents/com.orderly.rubheat.plist
```

#### 方法 3：服务器部署

推荐使用云服务器（AWS EC2、DigitalOcean、Heroku 等）：

1. 将项目上传到服务器
2. 配置环境变量（使用 `.env` 文件或系统环境变量）
3. 设置 cron 任务
4. 配置日志轮转（logrotate）

## 日志和监控

### 查看日志

脚本会生成两个日志文件：

- `orderly_bot.log`：详细的执行日志
- `replied_posts.json`：已回复的推文记录（自动去重）

查看最近的日志：

```bash
tail -f orderly_bot.log
```

### 日志内容

日志包含：
- 每次搜索的推文数量
- 每条回复的详细信息
- 成功/失败状态
- API 调用错误信息

## 注意事项

### API 限制

- Twitter API Basic Plan 每月有限制
- 建议设置每天执行一次，回复 5 条
- 脚本内置了 30-90 秒的随机延迟，避免触发速率限制

### 内容质量

- **定期更新素材库**：建议每周更新 `materials.json`
- **保持回复自然**：避免千篇一律的模板
- **选择优质推文**：只回复高质量、相关度高的推文

### 安全性

- **不要提交 `.env` 文件**到版本控制系统
- **使用环境变量**存储敏感信息
- **定期轮换 API 密钥**

## 故障排除

### 问题：无法找到符合条件的推文

**解决方案**：
- 检查搜索关键词是否过于严格
- 降低互动数阈值（修改代码中的 `likes > 50`）
- 扩大时间范围（修改 `age_days < 3`）

### 问题：API 认证失败

**解决方案**：
- 确认 `.env` 文件中的凭证正确
- 检查 Twitter Developer 账号是否激活
- 确认 App 是否有正确的权限（Read and Write）

### 问题：回复失败

**解决方案**：
- 检查是否超过 API 速率限制
- 确认账号没有被 Twitter 限制
- 查看日志获取详细错误信息

### 问题：Telegram 报告未发送

**解决方案**：
- 确认 Bot Token 和 Group ID 正确
- 检查机器人是否已加入群组
- 确认机器人有发送消息的权限

## 维护建议

### 每周任务

1. 更新 `materials.json` 中的推文链接
2. 添加新的文案素材
3. 检查日志，确认运行正常

### 每月任务

1. 分析回复效果（点赞、转发、关注）
2. 优化搜索关键词
3. 调整回复模板
4. 检查 API 使用量

## 进阶功能（可选）

### 集成 AI 生成回复

可以接入 OpenAI API 生成更自然的回复：

```bash
pip install openai
```

在代码中添加：

```python
import openai

def generate_ai_reply(post_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是 Orderly 的营销专员..."},
            {"role": "user", "content": f"为这条推文生成回复：{post_text}"}
        ]
    )
    return response.choices[0].message.content
```

### 数据分析

可以添加数据库记录所有回复的效果：

```bash
pip install sqlalchemy
```

记录每条回复的互动数据，定期分析效果。

## 支持

如有问题，请联系：
- 项目负责人：Aaron
- 邮箱：aaron@orderly.network

## 许可证

内部使用，保密。

---

**最后更新**：2026年2月11日
