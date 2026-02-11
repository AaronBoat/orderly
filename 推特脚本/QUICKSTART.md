# 快速开始指南

## 5 分钟快速配置

### 步骤 1: 安装依赖

```bash
cd /Users/aaron/orderly打工/推特脚本
pip3 install -r requirements.txt
```

### 步骤 2: 配置 API 凭证

1. **复制配置文件模板**

```bash
cp .env.example .env
```

2. **获取 Twitter API 凭证**

   - 访问 https://developer.x.com
   - 创建新 App
   - 获取以下 5 个凭证：
     - API Key
     - API Secret  
     - Access Token
     - Access Token Secret
     - Bearer Token

3. **编辑 `.env` 文件**

```bash
nano .env  # 或使用你喜欢的编辑器
```

填入你的凭证：

```bash
X_API_KEY=你的实际api_key
X_API_SECRET=你的实际api_secret
X_ACCESS_TOKEN=你的实际access_token
X_ACCESS_SECRET=你的实际access_secret
X_BEARER_TOKEN=你的实际bearer_token
```

### 步骤 3: 更新素材库

编辑 `materials.json`，将示例链接替换为实际推文：

```json
{
  "our_post_links": [
    "https://x.com/OrderlyCN_/status/1234567890123456789",
    "https://x.com/OrderlyNetwork/status/9876543210987654321"
  ]
}
```

### 步骤 4: 验证配置

运行配置验证脚本：

```bash
python3 check_config.py
```

如果所有检查都通过，你就可以运行机器人了！

### 步骤 5: 运行机器人

#### 方式 1: 使用快速启动脚本

```bash
./run_bot.sh
```

#### 方式 2: 直接运行 Python 脚本

```bash
python3 orderly_rub_heat_bot.py
```

## 设置定时任务（可选）

### macOS 使用 cron

编辑 crontab：

```bash
crontab -e
```

添加定时任务（每天上午 10:00）：

```cron
0 10 * * * cd /Users/aaron/orderly打工/推特脚本 && /usr/bin/python3 orderly_rub_heat_bot.py >> /Users/aaron/orderly打工/推特脚本/cron.log 2>&1
```

保存并退出。

查看已设置的任务：

```bash
crontab -l
```

## Telegram 报告（可选）

如果想接收每日运行报告：

1. 在 Telegram 找到 @BotFather
2. 创建新 Bot，获取 Token
3. 将 Bot 添加到群组
4. 获取群组 ID（使用 @userinfobot）
5. 在 `.env` 文件中添加：

```bash
TELEGRAM_TOKEN=你的bot_token
TELEGRAM_GROUP_ID=-1001234567890
```

## 常见命令

### 查看日志

```bash
# 实时查看日志
tail -f orderly_bot.log

# 查看最近 50 行
tail -50 orderly_bot.log

# 搜索错误
grep "ERROR" orderly_bot.log
```

### 检查已回复记录

```bash
# 查看已回复的推文 ID
cat replied_posts.json

# 清空已回复记录（小心使用！）
echo "[]" > replied_posts.json
```

### 更新依赖

```bash
pip3 install --upgrade -r requirements.txt
```

## 维护清单

### 每周一次

- [ ] 更新 `materials.json` 中的推文链接
- [ ] 检查日志确认运行正常
- [ ] 查看回复效果

### 每月一次

- [ ] 分析回复数据
- [ ] 优化文案和模板
- [ ] 检查 API 使用量
- [ ] 更新素材库内容

## 故障排除

### 问题：找不到推文

```bash
# 检查搜索是否正常
grep "搜索热门推文" orderly_bot.log
grep "找到.*候选推文" orderly_bot.log
```

**解决方案**：
- 降低点赞数阈值
- 扩大时间范围
- 调整搜索关键词

### 问题：API 认证失败

```bash
# 运行配置验证
python3 check_config.py
```

**解决方案**：
- 检查 `.env` 文件格式
- 确认凭证正确无误
- 检查 App 权限设置

### 问题：回复失败

```bash
# 查看错误详情
grep "ERROR" orderly_bot.log | tail -10
```

**解决方案**：
- 检查 API 速率限制
- 确认账号状态正常
- 查看具体错误信息

## 有用的链接

- Twitter Developer Portal: https://developer.x.com
- Tweepy 文档: https://docs.tweepy.org
- python-telegram-bot 文档: https://python-telegram-bot.org
- Cron 表达式生成器: https://crontab.guru

## 需要帮助？

查看完整文档：`README.md`

---

**提示**：首次运行建议在白天进行，以便观察运行情况并及时调整配置。
