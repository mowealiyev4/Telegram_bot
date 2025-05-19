import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY").strip()
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Mən Hamster Botam. Mənə yaz, cavab verim – amma real və qısa danışıram.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sən doğma, real və qısa danışan Telegram botusan."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        reply = response["choices"][0]["message"]["content"].strip()
        await update.message.reply_text(reply)
    except Exception as e:
        print("Xəta:", e)
        await update.message.reply_text("Xəta baş verdi. Yenidən yoxla.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
