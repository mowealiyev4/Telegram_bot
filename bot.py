import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request

# Ayarlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# /sohbet komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Məni ya tag elə, ya da cavab yaz. Mən də sənə dost kimi cavab verim.")

# Sadə test cavabı
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message:
        print("TEST LOG: mesaj gəldi -", message.text)
        await message.reply_text("Məni eşidirsənsə, deməli işləyirəm!")

# Handlerlər
telegram_app.add_handler(CommandHandler("sohbet", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook (DÜZGÜN async + await ilə)
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return "OK"

# Webhook qurulması
@app.route('/')
def index():
    bot = Bot(token=BOT_TOKEN)
    asyncio.run(bot.set_webhook(url=f"{WEBHOOK_URL}/webhook"))
    return "Webhook quruldu!"

# Serveri işə sal
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
