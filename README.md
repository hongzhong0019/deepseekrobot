# DeepSeek Telegram Bot (Free Starter)

一个可直接部署到 Railway/Render 的 Telegram 机器人示例，调用 DeepSeek Chat API。

> **不要把 API 密钥提交到 GitHub！** 使用 `.env`（本地测试）或在 Railway/Render 的环境变量里配置。

## 1) 本地运行（可选）
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 在项目根目录创建 .env 文件，内容参考 .env.example
python bot.py
```

## 2) 部署到 Railway（免费额度）
1. 新建项目，连接你的 GitHub 仓库。
2. 添加环境变量：`TELEGRAM_BOT_TOKEN`、`DEEPSEEK_API_KEY`。
3. 部署类型选择 **Worker**，启动命令为：`python bot.py`。

## 3) 重要
- 在 BotFather 关闭隐私模式（/setprivacy → Disable），让它在群组里也能正常处理消息。
- 不要把 `.env` 文件提交到仓库，已经在 `.gitignore` 中忽略。
