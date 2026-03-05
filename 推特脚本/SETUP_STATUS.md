# 🚀 OAuth 2.0 升级完成 - 使用指南

## ✅ 已完成的工作

### 1. 核心脚本

- ✅ **get_initial_token.py** - OAuth 2.0 初始授权脚本
- ✅ **orderly_rub_heat_bot_oauth2.py** - 支持自动 token 刷新的主脚本
- ✅ **test_oauth.py** - 完整的 OAuth 2.0 测试套件
- ✅ **check_setup.py** - 快速配置检查

### 2. 配置文件

- ✅ **.env** - 已配置 OAuth 2.0 凭证
- ✅ **materials.json** - 素材库（需更新链接）
- ✅ **requirements.txt** - 包含所有依赖

### 3. 文档

- ✅ **OAUTH2_GUIDE.md** - OAuth 2.0 详细指南
- ✅ **README.md** - 原始完整文档
- ✅ **QUICKSTART.md** - 快速开始指南

## 📊 当前状态

运行 `python3 check_setup.py` 的结果：

```
✅ 环境变量配置完整
ℹ️  需要获取 token（首次必须）
✅ 素材库已准备好
⚠️  4 个示例链接需要更新
✅ Python 依赖已安装
```

## 🎯 接下来的步骤

### 步骤 1: 获取 OAuth 2.0 Token（必须）

```bash
python3 get_initial_token.py
```

这个脚本会：
1. 显示一个授权 URL
2. 要求你在浏览器中访问并登录 X 账号
3. 授权后，浏览器会重定向到 `http://localhost:8080/callback?...`
4. 复制完整的 URL 并粘贴回终端
5. 自动生成 `token.json` 文件

**注意**：如果遇到 402 Payment Required 错误，说明：
- X Developer 账号可能需要升级到付费计划
- 或者 API 访问权限未激活
- 需要在 https://developer.x.com 检查账户状态

### 步骤 2: 更新素材库（推荐）

编辑 `materials.json`，将示例链接替换为实际推文：

```json
{
  "our_post_links": [
    "https://x.com/OrderlyCN_/status/实际推文ID",
    "https://x.com/OrderlyNetwork/status/实际推文ID"
  ]
}
```

### 步骤 3: 测试运行

```bash
# 测试配置
python3 test_oauth.py

# 如果测试通过，运行主脚本
python3 orderly_rub_heat_bot_oauth2.py
```

### 步骤 4: 设置定时任务

```bash
crontab -e

# 添加每天 10:00 运行
0 10 * * * cd /Users/aaron/orderly打工/推特脚本 && python3 orderly_rub_heat_bot_oauth2.py >> cron.log 2>&1
```

## 🔧 文件结构

```
推特脚本/
├── 核心脚本
│   ├── get_initial_token.py          # OAuth 2.0 初始化
│   ├── orderly_rub_heat_bot_oauth2.py # OAuth 2.0 主脚本
│   ├── orderly_rub_heat_bot.py       # OAuth 1.0a 旧脚本（备用）
│   ├── test_oauth.py                 # OAuth 2.0 测试
│   └── check_setup.py                # 快速检查
│
├── 配置文件
│   ├── .env                          # 实际凭证（已配置）
│   ├── .env.example                  # 凭证模板
│   ├── materials.json                # 素材库
│   ├── requirements.txt              # Python 依赖
│   └── token.json                    # OAuth 2.0 token（待生成）
│
├── 文档
│   ├── OAUTH2_GUIDE.md              # OAuth 2.0 指南
│   ├── README.md                    # 完整文档
│   ├── QUICKSTART.md                # 快速开始
│   ├── PROJECT_STRUCTURE.md         # 项目结构
│   └── X_API_USE_CASE.md           # API 申请文档
│
└── 运行时生成
    ├── orderly_bot.log              # 运行日志
    └── replied_posts.json           # 已回复记录
```

## 🆘 故障排除

### 问题 1: API 返回 402 Payment Required

**原因**：X Developer 账号没有 API 访问权限或余额不足

**解决方案**：
1. 访问 https://developer.x.com/en/portal/dashboard
2. 检查账号类型和 API 访问级别
3. 可能需要升级到 Basic Plan（$100/月）或更高

**替代方案**：
- 如果只是测试，可以使用模拟数据
- 或等待 API 访问权限激活

### 问题 2: Token 获取失败

**检查**：
1. Redirect URI 在 X Developer Portal 中正确配置
2. Client ID 和 Client Secret 正确
3. 复制的授权 URL 完整

### 问题 3: 导入错误

```bash
# 重新安装依赖
pip3 install -r requirements.txt --upgrade
```

## 📝 主要改进

### OAuth 2.0 vs OAuth 1.0a

| 特性 | 旧版本 (1.0a) | 新版本 (2.0) |
|------|--------------|--------------|
| 认证方式 | API Key + Secret | Client ID + Secret |
| Token 类型 | 永久 Access Token | 短期 Access Token (2h) |
| 自动刷新 | ❌ | ✅ Refresh Token |
| 安全性 | 中等 | 高 |
| 设置复杂度 | 简单 | 需要一次授权 |

### 新功能

1. **自动 Token 刷新**
   - Access token 过期时自动使用 refresh token 获取新的
   - 无需手动干预

2. **更好的错误处理**
   - 401/403 错误自动刷新 token 并重试
   - 详细的日志记录

3. **完整的测试套件**
   - 环境变量检查
   - Token 验证
   - API 连接测试
   - 素材库验证

## 🎓 学习资源

- **OAuth 2.0 官方文档**: https://oauth.net/2/
- **X API 文档**: https://developer.x.com/en/docs
- **Tweepy OAuth 2.0**: https://docs.tweepy.org/en/stable/authentication.html

## 📞 需要帮助？

1. **配置问题** → 运行 `python3 check_setup.py`
2. **Token 问题** → 查看 [OAUTH2_GUIDE.md](OAUTH2_GUIDE.md)
3. **API 错误** → 检查 `orderly_bot.log`
4. **使用指南** → 阅读 [README.md](README.md)

---

## ⚡ 快速命令参考

```bash
# 检查配置
python3 check_setup.py

# 获取 token（首次）
python3 get_initial_token.py

# 完整测试
python3 test_oauth.py

# 运行脚本
python3 orderly_rub_heat_bot_oauth2.py

# 查看日志
tail -f orderly_bot.log

# 检查 token
cat token.json
```

---

**最后更新**: 2026年2月11日  
**版本**: OAuth 2.0  
**状态**: ✅ 准备就绪，等待首次授权
