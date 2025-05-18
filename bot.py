import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

# Ətraf mühit dəyişənlərini oxuyur
BOT_TOKEN = os.getenv("7589791481:AAGKIsetT8xS66wp0zsshV_o_Gb_KhE-PzU")
OPENAI_API_KEY = os.getenv("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")

# OpenAI müştərisi
client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Mən Hamster Botam. Adımı tag etsən, cavab verərəm — amma çox danışmıram, yormuram, özüm kimi danışıram.")

# Mesajlara cavab
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sən bir insan kimi yazışan chatbot-san. Cavabların doğma, real və qısa olsun. Zarafat edə bilərsən. Dost kimi cavab ver."},
                {"role": "user", "content": text}
            ],
            max_tokens=50,
            temperature=0.8
        )
        await update.message.reply_text(response.choices[0].message.content.strip())

    except Exception as e:
        await update.message.reply_text("Xəta baş verdi.")

# Botu işə salır
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
