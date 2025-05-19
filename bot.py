from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import traceback

# AÇARLAR — **tokenləri istədiyin kimi dəyişə bilərsən**
BOT_TOKEN = "7589791481:AAFFdKbZKEJeS079ID0mnQk1d3yIdlckYDY"
BOT_USERNAME = "hamster_sohbet_bot"
OPENAI_API_KEY = "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"
BOT_NAME_KEYWORDS = ["hamster", "Hamster", "Hamster bot", "hamster bot"]

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Hamster Botam. Adımı tag etsən, ya reply etsən cavab verərəm — amma qısa danışıram, real kimi.")

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
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sən dostcasına yazışan bot-san. Cavabın 1 cümlə, real və qısa olsun."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50,
                temperature=0.9,
                stop=["\n"]
            )
            reply = response.choices[0].message.content.strip()
            await message.reply_text(reply)
        except Exception as e:
            await message.reply_text("Xəta baş verdi.")
            traceback.print_exc()

# BOTU BAŞLAT
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işləyir... Reply və tag ilə cavab verir.")
app.run_polling()
