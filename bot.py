import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# Tokenləri oxu
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# /sohbet komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Hamster Botam. Mənə yaz və ya repley at — cavab verim. Amma real və qısa danışıram."
    )

# Mesaj cavabı
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_text = None

    if message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id:
        user_text = message.text
    elif f"@{context.bot.username}" in message.text:
        user_text = message.text.replace(f"@{context.bot.username}", "").strip()
    elif message.chat.type == "private":
        user_text = message.text

    if not user_text:
        return  # Heç bir uyğun mesaj yoxdursa, cavab vermə

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "San bir insan kimi yazışan chatbot-san. Cavabların doğma, real və qısa olsun."},
                {"role": "user", "content": user_text},
            ],
            max_tokens=100,
            temperature=0.8,
        )
        await message.reply_text(response["choices"][0]["message"]["content"].strip())

    except Exception as e:
        print("OpenAI xətası:", e)
        await message.reply_text("Xəta baş verdi. Yenidən yoxla.")

# Botu qur
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
