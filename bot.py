import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 加载 .env（仅本地开发有用；在云端用环境变量）
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("deepseek-tg-bot")

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"  # 如果官方变更，请按文档调整

def ask_deepseek(query: str) -> str:
    """
    调用 DeepSeek Chat API，返回回复文本。
    """
    if not DEEPSEEK_API_KEY:
        return "服务器未配置 DEEPSEEK_API_KEY，请联系管理员。"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.7,
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        logger.exception("DeepSeek API request error")
        return f"调用 DeepSeek 失败：{e}"
    except Exception as e:
        logger.exception("DeepSeek API parse error")
        return f"解析 DeepSeek 响应失败：{e}"

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "你好！我是 DeepSeek Telegram 机器人。\n"
        "直接给我发消息即可调用 DeepSeek。\n"
        "命令：/help /ping"
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "使用方法：\n"
        "• 私聊：直接发送问题\n"
        "• 群组：@我 或者关闭隐私模式后直接说\n"
        "• /ping 测试是否在线"
    )

async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return
    text = update.message.text.strip()

    # 在群里：如果隐私模式是开启的，只有 @bot 或回复给 bot 的消息才能收到
    reply = ask_deepseek(text)
    await update.message.reply_text(reply)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("请设置 TELEGRAM_BOT_TOKEN 环境变量。")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("ping", cmd_ping))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot polling started...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
