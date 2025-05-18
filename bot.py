from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import traceback

# Ayarlar
BOT_USERNAME = "hamster_sohbet_bot"
BOT_NAME_KEYWORDS = ["hamster", "Hamster", "Hamster bot", "hamster bot"]

client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Mən Hamster Botam. Adımı tag etsən, cavab verərəm — amma çox danışmıram, yormuram, özüm kimi danışıram.")

# Cavablandırma funksiyası
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

        # “sus” yazılıbsa cavab vermə
        if user_input.lower() in ["sus", "sakit ol", "danışma"]:
            return

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Sən bir insan kimi yazışan chatbot-san. Cavabların doğma, real və qısa olmalıdır. "
                            "Yalnız 1 cümlə yaz. Rəsmi danışma, dost kimi ol. Zarafat edə bilərsən. Uzun izahlar vermə, robot kimi olma. "
                            "Əgər sözü başa düşmürsənsə, bunu bildirməlisən."
                        )
                    },
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

# Botu başlat
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işləyir (insan kimi qısa, reply ilə, zarafatla)...")
app.run_polling()
