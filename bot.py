import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# Tokenləri mühitdən götür
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Hamster Botam. Adımı tag etsən, cavab verərəm — amma çox danışmıram, yormuram, özüm kimi danışıram."
    )

# Mesajlara cavab
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Əgər mesaj boşdursa, cavab vermə
    if not text:
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "San bir insan kimi yazışan chatbot-san. Cavabların doğma, real və qısa olsun."},
                {"role": "user", "content": text}
            ],
            max_tokens=50,
            temperature=0.8
        )

        print(response)  # Debug üçün logda göstər

        # Cavabı çıxart (istənilən OpenAI cavab strukturunu dəstəkləyir)
        reply = ""
        if "choices" in response:
            if "message" in response["choices"][0]:
                reply = response["choices"][0]["message"]["content"]
            elif "text" in response["choices"][0]:
                reply = response["choices"][0]["text"]
            else:
                reply = "Cavab formatı anlaşılamadı."
        else:
            reply = "OpenAI cavabı boşdur."

        await update.message.reply_text(reply.strip())

    except Exception as e:
        await update.message.reply_text("Xəta baş verdi.")
        print("Xəta:", e)

# Botu işə salır
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
