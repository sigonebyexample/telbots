import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import PyPDF2
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# نصب nest_asyncio برای حل مشکل حلقه رویداد
nest_asyncio.apply()

# توکن ربات تلگرام
TOKEN = '8111787770:AAGJjC06KSfzdYxGvki7Mqsl06E7Snkqyl4'
translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام، عزیزم! لطفاً فایل PDF خود را ارسال کن.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.document.get_file()
    file_path = f"./{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    # خواندن متن از فایل PDF
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    # خلاصه کردن متن با Sumy
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)  # 5 جمله خلاصه

    summary_text = ' '.join(str(sentence) for sentence in summary)

    # ترجمه به فارسی
    translated_summary = translator.translate(summary_text, dest='fa').text
    await update.message.reply_text(translated_summary)

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_pdf))
    
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())