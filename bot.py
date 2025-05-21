import os
import traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

# Ayarlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# /sohbet komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Məni ya tag elə, ya da cavab yaz. Mən də səninlə doğma, qısa və ağıllı danışım — əsl dost kimi.")

# Cavab funksiyası
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
    print("Gelen mesaj:", user_input)

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
        print("Xəta baş verdi:", str(e))
        traceback.print_exc()
        await message.reply_text("Söz tapmadım, sən yenə bir yaz.")

# Başlat
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot işə düşdü.")
app.run_polling()
