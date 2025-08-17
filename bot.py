import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# 载入环境变量
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 机器人逻辑
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！我是 DeepSeek 机器人，发消息给我就能调用 DeepSeek 搜索。")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = " ".join(context.args)
    if not user_text:
        await update.message.reply_text("请输入要查询的问题，例如：/ask 今天的新闻")
        return
    
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": user_text}]}
    response = requests.post("https://api.deepseek.com/chat/completions", json=data, headers=headers)
    
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text(f"调用 DeepSeek 失败: {response.text}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"你说：{update.message.text}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
