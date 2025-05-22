import os
import traceback
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# Ayarlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Webhook-u tamamilə sil (bir dəfəlik)
bot = Bot(token=BOT_TOKEN)
try:
    bot.delete_webhook(drop_pending_updates=True)
    print("Webhook silindi.")
except Exception as e:
    print("Webhook silinərkən xəta baş verdi:", e)

# /sohbet komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Məni ya tag elə, ya da cavab yaz. Mən də səninlə doğma, ağıllı, qısa danışım — əsl dost kimi.")

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

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Sən çox ağıllı, səmimi, zarafatcıl, dürüst və doğma danışan bir bot dostsan. "
                    "Ana dilin Azərbaycan dilidir. Hər cavabın maksimum 1 cümlə olmalıdır, çox uzun yazma. "
                    "Cümlələrin real, maraqlı, düşündürücü və bir az da yumor dolu olsun, amma heç vaxt tərbiyəsizlik olmasın. "
                    "İnsan kimi cavab ver, robot tonunda olmasın. Hər sualı düzgün başa düş və dost kimi cavabla."
                )},
                {"role": "user", "content": user_input}
            ],
            max_tokens=50,
            temperature=0.95
        )
        reply = response.choices[0].message.content.strip()
        await message.reply_text(reply)
    except Exception:
        await message.reply_text("Söz tapmadım, sən yenə bir yaz.")
        traceback.print_exc()

# Botu işə sal
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("sohbet", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot polling ilə başladı...")
app.run_polling()
