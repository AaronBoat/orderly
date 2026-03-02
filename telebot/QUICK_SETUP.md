# 🎯 快速获取 Topic ID 并配置

## 当前状态
✅ Bot 已启动，`allowed_topics` 设为空列表（监听所有 Topic）
✅ 现在可以获取 Topic ID 了

## 📝 操作步骤

### 1️⃣ 在 Forum 的 updates Topic 发送一条测试消息
比如发送：`测试 updates`

### 2️⃣ 在 Forum 的 announcements Topic 发送另一条测试消息  
比如发送：`测试 announcements`

### 3️⃣ 查看 Bot 日志
```bash
screen -r telegram-bot
```

你会看到类似输出：
```
收到新消息 ID: 102950 from Chat: -1002011191127
消息来自 Topic ID: 102946，但不在允许列表中，跳过
如需监听此 Topic，请在 config.yaml 的 allowed_topics 中添加: 102946
```

**记录下两个 Topic 的 ID！**

按 `Ctrl+A` 然后按 `D` 退出日志查看

### 4️⃣ 编辑配置文件
```bash
vim config.yaml
```

找到 `allowed_topics` 部分，改为：
```yaml
allowed_topics:
  - 102946  # updates (替换为实际的 ID)
  - 102947  # announcements (替换为实际的 ID)
```

### 5️⃣ 重启 Bot
```bash
screen -X -S telegram-bot quit
./start_bot.sh
```

### 6️⃣ 测试
- 在 updates Topic 发消息 → 应该被翻译转发
- 在 announcements Topic 发消息 → 应该被翻译转发
- 在其他 Topic 发消息 → 应该被忽略（日志会显示）

## 🔍 查看效果
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

## ✅ 完成！
配置完成后，Bot 只会处理 updates 和 announcements 这两个 Topic 的消息。
