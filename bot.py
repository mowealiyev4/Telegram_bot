import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Hamster Botam. Adımı tag etsən, cavab verərəm — amma çox danışmıram, yormuram, özüm kimi danışıram."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "San bir insan kimi yazışan chatbot-san. Cavabların doğma, real və qısa olsun."},
                {"role": "user", "content": text}
            ],
            max_tokens=50,
            temperature=0.8
        )
        await update.message.reply_text(response.choices[0].message.content.strip())
    except Exception as e:
        await update.message.reply_text("Xəta baş verdi.")
        print(e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
