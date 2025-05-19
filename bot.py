from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import openai
import traceback

# Ayarlar
BOT_TOKEN = "7589791481:AAGyGE8ZISl9x-IdRnloGgClUWTl6uyzBmM"
BOT_USERNAME = "hamster_sohbet_bot"
BOT_NAME_KEYWORDS = ["hamster", "Hamster", "Hamster bot", "hamster bot"]
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Hamster Botam. Mənə yaz və ya reply et, ya da adımı tag etsən cavab verərəm — amma qısa danışaram, real kimi."
    )

# Cavablandırma
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.strip()
    called_by_tag = f"@{BOT_USERNAME.lower()}" in text.lower()
    called_by_name = any(name.lower() in text.lower() for name in BOT_NAME_KEYWORDS)
    called_by_reply = (
        message.reply_to_message and
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == context.bot.id
    )

    if called_by_tag or called_by_name or called_by_reply:
        user_input = text.replace(f"@{BOT_USERNAME}", "").strip()
        if user_input.lower() in ["sus", "sakit ol", "danışma"]:
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Qısa və doğma danış. Robot kimi yox. 1 cümlə. Zarafat edə bilərsən."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50,
                temperature=0.9
            )
            reply = response['choices'][0]['message']['content'].strip()
            await message.reply_text(reply)
        except Exception:
            await message.reply_text("Xəta baş verdi.")
            traceback.print_exc()

# Botu işə sal
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işə düşdü...")
app.run_polling()
