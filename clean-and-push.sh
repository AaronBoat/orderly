# 1. 备份当前目录（以防万一）
cp -r . ../orderly-backup

# 2. 创建一个全新的历史（无父提交）
git checkout --orphan fresh-main

# 3. 清空暂存区
git rm -rf .

# 4. 只添加 .md 和 .srt 文件（安全处理含空格/中文的路径）
find . -type f \( -name "*.md" -o -name "*.srt" \) -not -path "./.git/*" -print0 | xargs -0 git add

# 5. 添加 .gitignore
cat > .gitignore <<EOF
*.mov
*.mp4
*.zip
*.avi
.DS_Store
*[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].*
Orderly\ -\ *
EOF
git add .gitignore

# 6. 提交
git commit -m "docs: initial clean translation files (.md and .srt only)"

# 7. 强制推送到 main（因为远程是空的，这很安全）
git push -f origin fresh-main:main