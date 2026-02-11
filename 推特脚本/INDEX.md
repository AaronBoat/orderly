# Orderly 推特"蹭热点"自动化脚本

> 自动搜索热门推文并生成个性化回复，帮助 Orderly 推广品牌内容

## 🚀 快速开始

### 新手？从这里开始

1. **查看快速开始指南** → [QUICKSTART.md](QUICKSTART.md)
   
   5 分钟内完成配置并运行你的第一个任务

2. **阅读完整文档** → [README.md](README.md)
   
   详细的安装、配置、部署和维护指南

3. **了解项目结构** → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
   
   了解每个文件的作用和依赖关系

## 📋 三步开始

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 配置环境
cp .env.example .env
# 编辑 .env 填入你的 Twitter API 凭证

# 3. 运行机器人
./run_bot.sh
```

## 📁 主要文件

| 文件 | 说明 | 操作 |
|------|------|------|
| [orderly_rub_heat_bot.py](orderly_rub_heat_bot.py) | 主程序脚本 | 核心代码 |
| [materials.json](materials.json) | 素材库 | **需要更新** |
| [.env.example](.env.example) | 配置模板 | 复制为 `.env` |
| [check_config.py](check_config.py) | 配置验证 | 运行验证 |
| [run_bot.sh](run_bot.sh) | 快速启动 | 一键运行 |

## 🎯 核心功能

- ✅ 自动搜索 AI、RWA、DEX、交易等热门推文
- ✅ 智能生成个性化回复（避免垃圾信息）
- ✅ 自动去重，避免重复回复
- ✅ Telegram 每日报告
- ✅ 完整的日志记录
- ✅ 支持定时任务（cron）

## ⚙️ 配置要求

### 必需

- [x] Twitter/X Developer 账号和 API 凭证
- [x] Python 3.10+
- [x] 更新 `materials.json` 中的推文链接

### 可选

- [ ] Telegram Bot（用于接收报告）

## 🔧 常用命令

```bash
# 验证配置
python3 check_config.py

# 手动运行一次
python3 orderly_rub_heat_bot.py

# 使用启动脚本
./run_bot.sh

# 查看日志
tail -f orderly_bot.log

# 设置定时任务（每天 10:00）
crontab -e
# 添加: 0 10 * * * cd /path/to/script && python3 orderly_rub_heat_bot.py
```

## 📊 工作流程

```
1. 搜索热门推文
   ├─ 关键词: AI, RWA, DEX, trading, crypto
   ├─ 过滤: >50 赞, <3 天
   └─ 去重: 跳过已回复

2. 智能回复
   ├─ 检测主题 (RWA/Trading/AI)
   ├─ 选择合适的文案片段
   ├─ 生成个性化回复
   └─ 添加自然变化

3. 发布回复
   ├─ 发布到 Twitter
   ├─ 记录已回复 ID
   └─ 随机延迟 30-90 秒

4. 发送报告
   └─ Telegram 群聊报告（可选）
```

## ⚠️ 重要提醒

### 首次使用前必做

1. ✏️ **更新 materials.json**
   
   将 `EXAMPLE1`、`EXAMPLE2` 等替换为实际的推文链接

2. 🔐 **配置 .env 文件**
   
   填入你的 Twitter API 凭证

3. ✅ **运行配置验证**
   
   ```bash
   python3 check_config.py
   ```

### 安全注意事项

- 🚫 **不要提交 `.env` 文件** 到版本控制
- 🔒 **保护好 API 密钥** 不要分享
- 📝 **定期检查日志** 确保正常运行
- 🔄 **定期轮换密钥** 提高安全性

## 📈 维护建议

### 每周

- [ ] 更新 `materials.json` 中的推文链接
- [ ] 添加新的文案素材
- [ ] 检查运行日志

### 每月

- [ ] 分析回复效果
- [ ] 优化搜索关键词
- [ ] 调整回复模板
- [ ] 检查 API 使用量

## 🆘 需要帮助？

1. **配置问题** → 运行 `python3 check_config.py`
2. **运行错误** → 查看 `orderly_bot.log`
3. **详细文档** → 阅读 [README.md](README.md)
4. **快速指南** → 查看 [QUICKSTART.md](QUICKSTART.md)

## 📚 文档导航

- [QUICKSTART.md](QUICKSTART.md) - 快速开始（5 分钟配置）
- [README.md](README.md) - 完整文档（安装、部署、维护）
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
- [需求_AGENT.md](需求_AGENT.md) - 原始需求文档（英文）

## 📝 版本信息

- **版本**: 1.0.0
- **创建日期**: 2026年2月11日
- **Python**: 3.10+
- **依赖**: tweepy, python-telegram-bot, python-dotenv

## 📄 许可证

内部使用，保密。

---

**准备好了吗？** 开始阅读 [QUICKSTART.md](QUICKSTART.md) 进行配置！ 🚀
