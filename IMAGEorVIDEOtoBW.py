import cv2
import numpy as np
from collections import deque
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import imutils
import time

# محدوده رنگ سبز
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=64)

# تابعی برای پردازش تصویر
def process_image(image_path: str) -> str:
    # بارگذاری تصویر
    image = cv2.imread(image_path)

    # پردازش تصویر (به عنوان مثال، تبدیل به خاکستری)
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ذخیره تصویر پردازش شده
    processed_image_path = 'processed_image.jpg'
    cv2.imwrite(processed_image_path, processed_image)

    return processed_image_path

# تابعی برای پردازش ویدیو
def process_video(video_source: str) -> str:
    if video_source == "webcam":
        vs = cv2.VideoCapture(0)
    else:
        vs = cv2.VideoCapture(video_source)

    output_path = 'processed_video.avi'
   
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    time.sleep(2.0)

    while True:
        ret, frame = vs.read()
        if not ret:
            break
       
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
       
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
           
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        out.write(frame)

    vs.release()
    out.release()
   
    return output_path

# تابعی برای دریافت عکس یا ویدیو
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo:
        photo_file = update.message.photo[-1].get_file()
        await photo_file.download('temp_image.jpg')
       
        processed_image_path = process_image('temp_image.jpg')
        with open(processed_image_path, 'rb') as f:
            await update.message.reply_photo(photo=InputFile(f))
       
    elif update.message.video:
        video_file = update.message.video.get_file()
        await video_file.download('temp_video.mp4')
       
        processed_video_path = process_video('temp_video.mp4')
        with open(processed_video_path, 'rb') as f:
            await update.message.reply_video(video=InputFile(f))

# تابعی برای شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! لطفاً یک عکس یا ویدیو ارسال کنید.")

def main():
    # توکن API شما
    application = ApplicationBuilder().token("7764613583:AAGr3RuwZHHGl08F0EUp-rpEyIXefv0a-JE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

    application.run_polling()

if __name__ == '__main__':
    main()