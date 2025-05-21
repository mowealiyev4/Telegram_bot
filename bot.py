from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import traceback

# Ayarlar
BOT_TOKEN = "7589791481:AAHA7ceWMS4KcV0iQA6mKqqolOy8AdPNRWc"
BOT_USERNAME = "hamster_sohbet_bot"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Məni ya tag elə, ya da cavab yaz. Mən də səninlə doğma, qısa və ağıllı danışım — əsl dost kimi.")

# Cavablandırma funksiyası
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    is_reply = (
        message.reply_to_message and
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == context.bot.id
    )
    is_tagged = f"@{BOT_USERNAME.lower()}" in message.text.lower()

    if not (is_reply or is_tagged):
        return

    user_input = message.text.replace(f"@{BOT_USERNAME}", "").strip()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sənin ana dilin Azərbaycan dilidir və sən çox ağıllı, real, səmimi və doğma danışırsan. "
                        "Cavabların qısa olsun (maksimum 1 cümlə), amma məntiqli və düşündürücü. "
                        "Hər yazılanı düzgün anla və cavab ver. Robot kimi danışma, elə yaz ki, istifadəçi səni real biri zənn etsin. "
                        "Səmimi ol, zarafat edə bilərsən, amma həmişə dürüst və yerində danış."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            max_tokens=40,
            temperature=0.9
        )
        reply = response.choices[0].message.content.strip()
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text("Söz tapmadım, sən yenə bir yaz.")
        traceback.print_exc()

# Botu başlat
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot hazır: yalnız tag və reply cavab verir — Azərbaycan dilində, qısa, ağıllı və real.")
app.run_polling()
