import cv2
import numpy as np
from PIL import ImageGrab
from time import sleep
import pytesseract
import ctypes
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

from private_stuff import BOT_TOKEN

ALERT_SPAM_INTERVAL = 15  # time between messages when queue is over to WAKE YOU UP
WAKE_UP_MESSAGE = "YOU WANT TO WAIT ANOTHER 10 HOURS? NO? WAKE THE HELL UP"
# WAKE_UP_MESSAGE = "WTF AM I DOING WITH MY LIFE"
# WAKE_UP_MESSAGE = "I MUST KISS MY PARTNER FOR PUTTING UP WITH THIS. HOW DOES ONE PUT UP WITH THIS?"

# pytesseract executeable location from https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# assumes WoW is running under Windows (tested on Win 10 Pro)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# if the above method for screen size detection didn't work, remove it  and uncomment your screen resolution

# screensize = (3840, 2160)
# screensize = (2560, 1440)
# screensize = (1920, 1080)

print("screensize: " + str(screensize))

center_x = screensize[0] / 2
center_y = screensize[1] / 2

x_margin = screensize[0] / 10
y_margin = screensize[1] / 12

queue_msg_box = center_x - x_margin, \
                center_y - y_margin, \
                center_x + x_margin, \
                center_y + y_margin

# Edit False to True to see this program running with a preview
test_run = False

while test_run:
    test_np_image_grab = np.array(ImageGrab.grab(bbox=queue_msg_box))
    test_hsv_image = cv2.cvtColor(test_np_image_grab, cv2.COLOR_BGR2HSV)

    cv2.imshow('preview', test_hsv_image)
    # character recognition happens HERE
    ocr_string = pytesseract.image_to_string(test_hsv_image)
    print(ocr_string)

    if cv2.waitKey(25) and 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    sleep(1)


def spam_user(bot, job):
    bot.send_message(job.context, text=WAKE_UP_MESSAGE)


def get_queue_postion_from_screen():
    single_np_image_grab = np.array(ImageGrab.grab(bbox=queue_msg_box))
    single_hsv_image = cv2.cvtColor(single_np_image_grab, cv2.COLOR_BGR2HSV)
    return pytesseract.image_to_string(single_hsv_image)


# telegram bot stuff

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def get_position(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=get_queue_postion_from_screen())


def start_alarm(bot, update, job_queue, chat_data):

    def check_if_queue_inactive():
        queue_is_active = True

        np_image_grab = np.array(ImageGrab.grab(bbox=queue_msg_box))

        hsv_image = cv2.cvtColor(np_image_grab, cv2.COLOR_BGR2HSV)
        # cv2.imshow('preview', hsv_image)

        # character recognition happens HERE
        ocr_string = pytesseract.image_to_string(hsv_image)
        ocr_length = len(ocr_string)
        print(ocr_length)

        if ocr_length < 40:
            queue_is_active = False

        if not queue_is_active:
            return True
        else:
            return False

    chat_id = update.message.chat_id

    update.message.reply_text('Alarm successfully started!')

    queue_active = True

    while queue_active:
        if check_if_queue_inactive():
            queue_active = False
        else:
            sleep(5)
    else:
        # executed when while condition becomes false
        job = job_queue.run_repeating(spam_user, ALERT_SPAM_INTERVAL, context=chat_id)
        chat_data['job'] = job


def stop_alarm(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Alarm successfully stopped!')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# enter your token here
telegram_token = BOT_TOKEN

updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
position_handler = CommandHandler('pos', get_position)
start_alarm_handler = CommandHandler('startalarm',
                                     start_alarm,
                                     pass_job_queue=True,
                                     pass_chat_data=True)
stop_alarm_handler = CommandHandler("unset", stop_alarm, pass_chat_data=True)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(position_handler)
dispatcher.add_handler(start_alarm_handler)
dispatcher.add_handler(stop_alarm_handler)

# log all errors
dispatcher.add_error_handler(error)

# Start the Bot

updater.start_polling()
updater.idle()
