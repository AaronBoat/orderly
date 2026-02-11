# 项目文件说明

## 核心文件

### 📜 orderly_rub_heat_bot.py
主程序脚本，包含所有核心功能：
- 搜索热门推文
- 生成回复内容
- 发布回复
- 发送 Telegram 报告
- 日志记录

### 📊 materials.json
素材库文件，包含：
- RWA 相关文案片段
- 交易相关文案片段
- 回复模板
- Orderly 账号列表
- 推文链接

**重要**：需要定期更新推文链接和文案内容。

### 📋 requirements.txt
Python 依赖包列表：
- tweepy: Twitter API 客户端
- python-telegram-bot: Telegram Bot API
- python-dotenv: 环境变量加载

## 配置文件

### 🔐 .env.example
环境变量模板文件，包含所需的 API 凭证说明。
使用时需复制为 `.env` 并填入实际值。

### 🚫 .gitignore
Git 忽略文件，防止敏感信息被提交：
- `.env` 文件
- 日志文件
- Python 缓存
- 已回复记录

## 辅助脚本

### ✅ check_config.py
配置验证脚本，用于检查：
- 环境变量是否正确配置
- 素材库格式是否正确
- Twitter API 连接是否正常
- Telegram Bot 是否可用

运行：`python3 check_config.py`

### 🚀 run_bot.sh
快速启动脚本（Bash），自动完成：
- 检查 Python 环境
- 创建虚拟环境
- 安装依赖
- 检查配置
- 运行主程序

运行：`./run_bot.sh`

## 文档文件

### 📖 README.md
完整的项目文档，包含：
- 功能特性说明
- 详细的安装步骤
- 使用方法和部署指南
- 故障排除
- 维护建议

### ⚡ QUICKSTART.md
快速开始指南，提供：
- 5 分钟快速配置
- 常用命令
- 维护清单
- 简化的故障排除

### 📝 需求_AGENT.md
原始需求文档（英文），详细描述了项目需求和技术方案。

## 运行时生成的文件

这些文件在运行时自动生成，已被 `.gitignore` 忽略：

### 📝 orderly_bot.log
详细的运行日志，记录：
- 每次执行的时间
- 搜索到的推文
- 生成的回复
- 成功/失败状态
- 错误信息

### 📋 replied_posts.json
已回复的推文 ID 列表，用于：
- 避免重复回复
- 自动去重
- 保留最近 100 条记录

### 🔒 .env
实际的环境变量配置文件（敏感信息），包含：
- Twitter API 凭证
- Telegram Bot 配置

**重要**：此文件不应提交到版本控制系统！

## 文件依赖关系

```
orderly_rub_heat_bot.py
    ├── 读取 .env （环境变量）
    ├── 读取 materials.json （素材库）
    ├── 读取/写入 replied_posts.json （去重）
    └── 写入 orderly_bot.log （日志）

check_config.py
    ├── 读取 .env （验证配置）
    └── 读取 materials.json （验证格式）

run_bot.sh
    └── 调用 orderly_rub_heat_bot.py
```

## 使用建议

### 首次使用

1. 阅读 `QUICKSTART.md`
2. 配置 `.env` 文件
3. 更新 `materials.json`
4. 运行 `check_config.py` 验证
5. 运行 `./run_bot.sh` 测试

### 日常使用

1. 定期更新 `materials.json`
2. 查看 `orderly_bot.log` 监控运行
3. 清理 `replied_posts.json`（可选）

### 问题排查

1. 运行 `check_config.py` 检查配置
2. 查看 `orderly_bot.log` 了解详情
3. 参考 `README.md` 故障排除部分

## 文件大小参考

- 主程序：~10 KB
- 素材库：~2 KB
- 日志文件：随时间增长（建议定期清理）
- 已回复记录：~2 KB（自动限制 100 条）

## 安全提醒

⚠️ **敏感文件**：
- `.env` - 包含 API 密钥，绝不能分享或提交
- `orderly_bot.log` - 可能包含敏感信息，注意保护

✅ **可分享文件**：
- `.env.example` - 仅包含模板，安全
- `materials.json` - 营销文案，可以分享
- 所有文档和脚本 - 不含敏感信息

---

**最后更新**：2026年2月11日
