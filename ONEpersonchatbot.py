import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# نصب nest_asyncio برای حل مشکل حلقه رویداد
nest_asyncio.apply()

TOKEN = '7314437224:AAHLxUA8RUuSirB3m-oK84j1yYXij8xc-vs'

responses = {
    "چطوری": "خوبم، عزیزم! تو چطوری؟",
    "دوستت دارم": "من هم تو را خیلی دوست دارم!",
    "کار": "کار دارم، اما همیشه برای تو وقت دارم.",
    "خبر": "هیچی خاصی نیست، فقط به تو فکر می‌کنم.",
    "آب و هوا": "آب و هوا خوبه، اما من بیشتر نگران تو هستم.",
    "اسم تو چیه؟": "من حسین هستم، اما تو می‌تونی منو هرطور که دوست داری صدا کنی.",
    "چرا اینجا هستی؟": "برای اینکه به تو نزدیک باشم و به سوالاتت پاسخ بدم.",
    "عاشقانه‌ترین لحظه ما": "هر لحظه‌ای که با تو گذرانده‌ام، برایم خاص است.",
    "نظرت درباره عشق چیه؟": "عشق زیباترین احساسی است که می‌توان تجربه کرد.",
    "چی دوست داری بخوری؟": "هر چیزی که با تو بخورم، خوشمزه است!",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام، عزیزم! چی می‌خواهی بپرسی؟")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    response = responses.get(user_message, "متاسفم، نمی‌توانم به این سوال پاسخ دهم.")
    await update.message.reply_text(response)

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
