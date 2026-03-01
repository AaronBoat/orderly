在 2026 年的当前环境下，**Gemini 3.1 Flash**（即 Nano Banana 2）已经发布，它是目前处理此类任务的性价比首选。

为了让 AI Agent（如 Cline, Cursor 或 GPT-4/Gemini 3.1）能为你写出高质量、无 Bug 的代码，你需要提供一份结构严谨、逻辑闭环的 **PRD（产品需求文档）**。

以下是为你准备的**最优需求文档模板**。你可以直接复制给你的 Agent。

---

# 需求文档：Telegram 群公告 AI 翻译转发机器人

## 1. 项目背景

开发一个基于 Python 的 Telegram Bot，实时监听源群组（Source Group/Channel）的公告，通过 Gemini 3.1 Flash API 将其翻译为中文，并保留原格式转发到目标群组（Target Group）。

## 2. 技术栈要求

* **语言：** Python 3.10+
* **Telegram 框架：** `python-telegram-bot` (v21.0+)
* **AI 接口：** Google Gemini API (`google-generativeai` 库)
* **模型选择：** `gemini-2.5-flash` 或 `gemini-3.1-flash` (优先)
* **并发处理：** 必须使用 `asyncio` 异步处理

## 3. 核心功能需求

### F1: 消息监听与过滤

* **监听范围：** 仅处理来自配置文件中 `SOURCE_CHAT_ID` 的消息。
* **消息类型：** 支持文本、图片+文字说明（Caption）。
* **去重逻辑：** 记录最近 50 条消息 ID，防止网络波动导致的重复触发。

### F2: AI 翻译策略

* **Prompt 设定：** > "你是一个专业的翻译官。请将输入的 Telegram 消息翻译成中文。要求：保持原有的 Emoji 位置，保留专有名词（如项目名、代码），语言风格要自然、符合中文社交媒体习惯。仅返回翻译后的文本，不要有任何解释说明。"
* **长文本处理：** 若消息超过 2000 字符，需自动拆分发送，确保不触发 Telegram 接口限制。

### F3: 转发与格式保留

* **格式对齐：** 如果原消息有图片，必须使用 `copy_message` 或重新上传图片，并将翻译后的文本作为 `caption` 发送。
* **链接保留：** 确保原消息中的 Markdown 链接在翻译后依然有效。

## 4. 异常处理与稳定性

* **重试机制：** 若 Gemini API 调用失败，需支持指数退避重试（最多 3 次）。
* **日志记录：** 记录每条转发的 `Source ID`、`Time` 以及 `Status`（成功/失败原因）。
* **速率限制：** 遵守 Telegram 的频率限制（每秒不超过 30 条消息）。

## 5. 配置文件 (config.yaml)

Agent 需要生成如下结构的配置文件模板：

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  source_chat_id: -100xxxxxx  # 公告群 ID
  target_chat_id: -100xxxxxx  # 中文群 ID
gemini:
  api_key: "YOUR_GEMINI_API_KEY"
  model_name: "gemini-3.1-flash"
settings:
  language: "zh-CN"

```

## 6. 交付目标

1. 包含完整注释的 `main.py`。
2. `requirements.txt`。
3. 简易的 `README.md` 说明如何获取 Chat ID 以及运行 Bot。

---

### 💡 为什么这份文档对 Agent 是“最优”的？

1. **明确了具体的库版本：** 避免 Agent 使用过时的旧版语法。
2. **定义了 Prompt：** 翻译质量 80% 取决于 Prompt，直接给它省去了它盲目猜测的过程。
3. **考虑了工程细节：** 如“图片 Caption 转发”、“长文本拆分”、“重试机制”，这些是新手容易忽略但上线必出问题的坑。

**如果你准备好了，我可以帮你直接根据这个文档生成第一版代码吗？**