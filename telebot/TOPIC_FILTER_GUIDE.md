# 如何配置 Forum Topic 过滤

## 问题
你的源群组是一个 Telegram Forum，里面有多个 Topic（子频道），但你只想监听和翻译特定的 Topic，比如：
- `updates` 
- `announcements`

## 解决方案

### 步骤 1: 获取 Topic ID

在 Telegram Forum 中，每个 Topic 都有一个唯一的 ID（`message_thread_id`）。

**方法 1：通过日志查看（推荐）**

1. 临时修改 `config.yaml`，将 `allowed_topics` 设为空列表或注释掉：
```yaml
allowed_topics: []
# 或者注释掉整个 allowed_topics 部分
```

2. 启动 Bot：
```bash
./start_bot.sh
```

3. 查看日志：
```bash
screen -r telegram-bot
```

4. 在 Forum 的 `updates` 和 `announcements` Topic 中各发一条测试消息

5. 查看日志输出，会显示类似：
```
收到新消息 ID: 12345 from Chat: -1002011191127
消息来自 Topic ID: 102946，但不在允许列表中，跳过
如需监听此 Topic，请在 config.yaml 的 allowed_topics 中添加: 102946
```

6. 记录下两个 Topic 的 ID

**方法 2：通过 RawDataBot**

1. 在 Forum 中添加 [@RawDataBot](https://t.me/RawDataBot)
2. 在 `updates` Topic 中发送消息
3. Bot 返回的 JSON 中查找 `message_thread_id`
4. 记录这个 ID
5. 在 `announcements` Topic 重复步骤 2-4

### 步骤 2: 配置 allowed_topics

编辑 `config.yaml`，添加获取到的 Topic ID：

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  source_chat_id: -1002011191127
  
  # 只监听这些 Topic ID
  allowed_topics:
    - 102946  # updates topic
    - 102947  # announcements topic
  
  target_chat_id: -1002266428094
```

### 步骤 3: 重启 Bot

```bash
screen -X -S telegram-bot quit
./start_bot.sh
```

### 步骤 4: 测试

1. 在 `updates` Topic 发送测试消息 → 应该被翻译转发
2. 在 `announcements` Topic 发送测试消息 → 应该被翻译转发  
3. 在其他 Topic 发送消息 → 应该被忽略

查看日志确认：
```bash
screen -r telegram-bot
```

应该看到：
```
收到新消息 ID: xxxxx from Chat: -1002011191127
消息来自允许的 Topic ID: 102946
翻译成功 (尝试 1/3)
消息 xxxxx 翻译转发成功
```

## 配置选项说明

### 监听所有 Topic
```yaml
allowed_topics: []
```
或完全注释掉 `allowed_topics` 部分

### 监听特定 Topic
```yaml
allowed_topics:
  - 102946
  - 102947
```

### 监听单个 Topic
```yaml
allowed_topics:
  - 102946
```

## 常见问题

### Q: 如何知道 Topic 的名称对应哪个 ID？
A: 目前最可靠的方法是通过日志。在该 Topic 发送消息后，日志会显示 Topic ID。你可以做个记录：
```
102946 → updates
102947 → announcements
```

### Q: 如果 Topic 名称改了，ID 会变吗？
A: 不会。Topic ID 是固定的，即使 Topic 名称更改，ID 也不会变。

### Q: 可以用 Topic 名称而不是 ID 吗？
A: 目前由于 Telegram Bot API 的限制，无法直接通过 API 获取 Topic 名称，只能使用 Topic ID。

### Q: Bot 没有反应怎么办？
A: 
1. 确认 Bot 在 Forum 中是管理员
2. 确认 Bot 的 Group Privacy 已关闭（@BotFather）
3. 查看日志：`screen -r telegram-bot`
4. 运行测试：`python3 test_bot.py`

## 快速开始示例

```bash
# 1. 先获取 Topic ID（临时监听所有）
vim config.yaml  # 设置 allowed_topics: []
./start_bot.sh
screen -r telegram-bot  # 查看日志，在各个 Topic 发消息获取 ID

# 2. 配置 Topic 过滤
vim config.yaml  # 添加获取到的 Topic ID
screen -X -S telegram-bot quit
./start_bot.sh

# 3. 测试
screen -r telegram-bot  # 查看日志，确认只处理指定 Topic
```
