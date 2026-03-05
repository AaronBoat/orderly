# OAuth 2.0 快速开始指南

## 🚀 三步配置 OAuth 2.0

### 步骤 1: 安装依赖

```bash
cd /Users/aaron/orderly打工/推特脚本
pip3 install -r requirements.txt
```

### 步骤 2: 配置 API 凭证

.env 文件已经包含你的凭证，确保以下值正确：

```bash
X_CLIENT_ID=N1BNdFR6bTZpUVBvN25YbjlVZ3g6MTpjaQ
X_CLIENT_SECRET=XJ6sKBTH0HCSDdbEp_EZtOmDEZKCny1YOoB-Y4VM6_g2U6TEKN
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAO8S7gEAAAAA%2Bi%2FSSko3GjkmWGXUnYd8PcnJLGM%3DY1VAr1qUGUwos1OlidSPEqF2wS1MefBXHjaqY67vaHHAVo4u1Q
X_REDIRECT_URI=http://localhost:8080/callback
```

### 步骤 3: 获取初始 Token（首次必须）

```bash
python3 get_initial_token.py
```

这个脚本会：
1. 生成一个授权 URL
2. 打开浏览器访问该 URL
3. 登录 X 账号并授权
4. 浏览器会重定向到 `http://localhost:8080/callback?state=...&code=...`
5. 复制完整的 URL 并粘贴到终端
6. 脚本会自动生成 `token.json` 文件

**重要**：这一步只需要做一次！token.json 会包含 access_token 和 refresh_token，脚本会自动刷新。

### 步骤 4: 测试配置

```bash
python3 test_oauth.py
```

这会测试：
- ✅ 环境变量配置
- ✅ Token 文件
- ✅ 搜索功能
- ✅ 用户认证
- ✅ 素材库

### 步骤 5: 运行主脚本

```bash
python3 orderly_rub_heat_bot_oauth2.py
```

## 🔄 OAuth 2.0 vs OAuth 1.0a

### 为什么要升级到 OAuth 2.0？

| 特性 | OAuth 1.0a | OAuth 2.0 |
|------|-----------|-----------|
| Token 过期 | 永不过期 | 2 小时后过期 |
| 自动刷新 | ❌ 不支持 | ✅ 支持 refresh_token |
| 设置复杂度 | 简单 | 需要一次性授权 |
| 安全性 | 较低 | 更高 |
| X 推荐 | ⚠️ 逐步淘汰 | ✅ 推荐使用 |

### OAuth 2.0 的优势

1. **自动刷新**：access_token 过期后自动使用 refresh_token 获取新的
2. **更安全**：短期 token 降低泄露风险
3. **符合标准**：X 官方推荐的认证方式

## 📁 文件说明

### 新增文件

- **get_initial_token.py** - 首次获取 OAuth 2.0 token
- **orderly_rub_heat_bot_oauth2.py** - 使用 OAuth 2.0 的主脚本
- **test_oauth.py** - OAuth 2.0 配置测试
- **token.json** - 存储 access_token 和 refresh_token（自动生成）

### 旧文件（兼容）

- **orderly_rub_heat_bot.py** - 使用 OAuth 1.0a 的旧脚本（仍可用）
- **check_config.py** - 配置检查（OAuth 1.0a）

## 🔧 常见问题

### Q: 为什么需要手动授权？

A: OAuth 2.0 需要用户授权才能获得发帖权限。这是 X 的安全要求，只需要做一次。

### Q: token.json 丢失怎么办？

A: 重新运行 `python3 get_initial_token.py` 获取新的 token。

### Q: Access token 过期了怎么办？

A: 脚本会自动使用 refresh_token 刷新，无需手动操作。

### Q: 如何查看 token 是否有效？

A: 运行 `python3 test_oauth.py` 测试所有配置。

### Q: 可以使用旧的 OAuth 1.0a 脚本吗？

A: 可以，但建议升级到 OAuth 2.0。旧脚本使用：
```bash
python3 orderly_rub_heat_bot.py
```

## 📊 测试流程

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 获取 token（首次）
python3 get_initial_token.py

# 3. 测试配置
python3 test_oauth.py

# 4. 运行一次测试
python3 orderly_rub_heat_bot_oauth2.py

# 5. 查看日志
tail -f orderly_bot.log
```

## ⚠️ 注意事项

### Token 管理

1. **token.json 包含敏感信息**，不要分享或提交到 Git
2. 已添加到 .gitignore，确保不会意外提交
3. Access token 每 2 小时过期，脚本会自动刷新
4. Refresh token 长期有效，妥善保管

### 授权范围

脚本请求的权限（Scopes）：
- `tweet.read` - 读取推文
- `tweet.write` - 发布推文和回复
- `users.read` - 读取用户信息
- `offline.access` - 获取 refresh_token

## 🎯 下一步

1. ✅ 确认所有测试通过
2. 📝 更新 materials.json 中的推文链接
3. ⏰ 设置 cron 定时任务
4. 📊 监控 orderly_bot.log

```bash
# 设置每天 10:00 运行
crontab -e
# 添加：
0 10 * * * cd /Users/aaron/orderly打工/推特脚本 && python3 orderly_rub_heat_bot_oauth2.py >> cron.log 2>&1
```

---

**准备好了？** 开始运行 `python3 get_initial_token.py` 🚀
