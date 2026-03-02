# Telegram 群公告 AI 翻译转发机器人

一个基于 Python 的 Telegram Bot，能够实时监听源群组（Source Group/Channel）的公告，通过 Gemini AI 将其翻译为中文，并保留原格式转发到目标群组（Target Group）。

## 功能特点

- ✅ **实时监听**：自动监听指定群组的所有消息
- ✅ **智能翻译**：使用 Google Gemini API 进行高质量翻译
- ✅ **格式保留**：支持文本、图片+说明、视频、文档等多种消息类型
- ✅ **去重机制**：记录最近 50 条消息，避免重复处理
- ✅ **重试机制**：API 调用失败时支持指数退避重试（最多 3 次）
- ✅ **长文本处理**：自动拆分超长消息，避免触发 Telegram 限制
- ✅ **异步处理**：使用 asyncio 实现高效并发

## 环境要求

- Python 3.10 或更高版本
- Telegram Bot Token
- Google Gemini API Key

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 获取必要的凭证

#### 2.1 创建 Telegram Bot

1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 命令并按提示操作
3. 复制获得的 Bot Token（格式：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）
4. 发送 `/mybots` → 选择你的 Bot → **Bot Settings** → **Group Privacy** → **Turn off**
   - 这一步是为了让 Bot 能够读取群组消息

#### 2.2 将 Bot 加入群组

**重要：Bot 必须在两个群组中都是管理员才能正常工作！**

**方法 1：通过 Bot 用户名添加（推荐）**

1. 打开你要添加 Bot 的群组
2. 点击群组名称，进入群组信息页面
3. 点击 **Add Members**（添加成员）或 **Administrators**（管理员）
4. 在搜索框中输入你的 Bot 用户名（例如：`@YourBotName_bot`）
5. 选择你的 Bot 并添加
6. **重要：将 Bot 设为管理员**，并给予以下权限：
   - ✅ Delete Messages（删除消息）- 可选
   - ✅ Restrict Members（限制成员）- 可选
   - ✅ Invite Users（邀请用户）- 可选
   - ✅ Pin Messages（置顶消息）- 可选
   - ✅ Manage Video Chats（管理视频聊天）- 可选
   - **注意：Bot 默认就能读取消息和发送消息，无需特别勾选**

7. 重复以上步骤，将 Bot 同时加入源群组和目标群组

**方法 2：通过邀请链接**

1. 在 @BotFather 中找到你的 Bot
2. 发送 `/mybots` → 选择你的 Bot
3. 点击 **Bot Settings** → **Inline Mode** → **Turn on**（如果需要）
4. 在群组中直接输入 `@YourBotName_bot`，然后添加为成员
5. 同样需要将 Bot 提升为管理员

**方法 3：使用 Bot 邀请链接（适用于频道）**

1. 进入频道设置
2. 点击 **Administrators**（管理员）
3. 点击 **Add Admin**（添加管理员）
4. 搜索并添加你的 Bot
5. 给予必要的权限（至少需要 **Post Messages** 权限）

**验证 Bot 是否成功加入：**

- 在群组中发送 `/start` 或任意消息
- 如果 Bot 是管理员，它应该能看到所有消息
- 查看群组成员列表，确认 Bot 在"管理员"列表中

#### 2.3 获取群组 Chat ID

有以下几种方法：

**方法 1：使用 @userinfobot（推荐）**

1. 确保你的 Bot 已经加入到源群组和目标群组，并设为管理员（参考上一步）
2. 在 Telegram 搜索 [@userinfobot](https://t.me/userinfobot)
3. 将群组的任意消息转发给 @userinfobot
4. Bot 会返回群组 ID（格式：`-100xxxxxxxxxx`）

**方法 2：使用 @RawDataBot**

1. 将 [@RawDataBot](https://t.me/RawDataBot) 加入群组
2. 在群组中发送任意消息
3. Bot 会返回完整的 JSON 数据，查找 `"id"` 字段

**方法 3：通过 Bot API**

临时运行以下代码：

```python
from telegram import Bot
import asyncio

async def get_chat_id():
    bot = Bot(token="YOUR_BOT_TOKEN")
    updates = await bot.get_updates()
    for update in updates:
        print(update)

asyncio.run(get_chat_id())
```

#### 2.4 获取 Gemini API Key

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录你的 Google 账号
3. 点击 **Create API Key** 创建新的 API Key
4. 复制生成的 Key（注意：Key 只会显示一次，请妥善保存）

### 3. 配置 Bot

复制配置文件模板：

```bash
cp config.yaml.example config.yaml
```

然后编辑 `config.yaml` 文件：

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"  # 替换为你的 Bot Token
  source_chat_id: -100xxxxxx    # 替换为源群组 ID
  target_chat_id: -100xxxxxx    # 替换为目标群组 ID

gemini:
  api_key: "YOUR_GEMINI_API_KEY"  # 替换为你的 Gemini API Key
  model_name: "gemini-2.0-flash-exp"  # 可选：gemini-1.5-flash

settings:
  language: "zh-CN"
```

### 4. 运行 Bot

```bash
python main.py
```

成功启动后，你会看到类似以下日志：

```
2026-03-01 10:00:00 - __main__ - INFO - 配置加载成功
2026-03-01 10:00:00 - __main__ - INFO - 机器人启动中...
```

## 运行建议

### 使用 Screen/tmux 保持后台运行

```bash
# 使用 screen
screen -S telegram-bot
python main.py
# 按 Ctrl+A 然后按 D 分离会话

# 重新连接
screen -r telegram-bot
```

### 使用 systemd 服务（Linux）

创建 `/etc/systemd/system/telegram-bot.service`：

```ini
[Unit]
Description=Telegram Translation Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telebot
ExecStart=/usr/bin/python3 /path/to/telebot/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

## 注意事项

1. **权限设置**：确保 Bot 在两个群组中都是管理员，且有以下权限：
   - 读取消息历史
   - 发送消息
   - 发送媒体文件

2. **速率限制**：
   - Telegram：每秒最多 30 条消息
   - Gemini API：免费版每分钟 15 次请求（具体限制请查看 [Google AI Studio](https://ai.google.dev/pricing)）

3. **隐私安全**：
   - ⚠️ **重要：`config.yaml` 已在 `.gitignore` 中，不会被上传到 GitHub**
   - 只有 `config.yaml.example` 模板会被提交到仓库
   - 首次使用时运行 `cp config.yaml.example config.yaml` 创建配置文件
   - 永远不要将真实的 API Key 和 Token 提交到公开仓库

4. **错误处理**：
   - 如果翻译失败，Bot 会自动转发原消息
   - 所有错误都会记录在日志中

## 常见问题

### 如何将 Bot 加入群组？

请参考 [2.2 将 Bot 加入群组](#22-将-bot-加入群组) 章节，里面有三种详细的添加方法。记得将 Bot 设为管理员！

### Bot 无法读取群组消息

确保你在 @BotFather 中关闭了 **Group Privacy**：
- `/mybots` → 选择 Bot → **Bot Settings** → **Group Privacy** → **Turn off**

### 翻译失败提示 API Key 错误

1. 检查 `config.yaml` 中的 `api_key` 是否正确
2. 确认 API Key 在 [Google AI Studio](https://makersuite.google.com/app/apikey) 中是启用状态
3. 检查网络连接是否能访问 Google 服务

### 消息没有被转发

1. 确认 Bot 在两个群组中都是管理员
2. 检查 `source_chat_id` 和 `target_chat_id` 是否正确
3. 查看日志输出，确认消息是否被正确接收

### 如何停止 Bot

- 直接运行：按 `Ctrl+C`
- Screen 会话：先 `screen -r telegram-bot`，然后按 `Ctrl+C`
- Systemd 服务：`sudo systemctl stop telegram-bot`

## 项目结构

```
telebot/
├── main.py              # 主程序
├── config.yaml          # 配置文件（需自行配置）
├── requirements.txt     # Python 依赖
└── README.md           # 本文档
```

## 技术栈

- **Telegram Bot**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21.0
- **AI 翻译**: [Google Gemini API](https://ai.google.dev/)
- **异步处理**: asyncio
- **配置管理**: PyYAML

## 许可证

本项目仅供学习和个人使用。

## 支持

如有问题或建议，请提交 Issue。
