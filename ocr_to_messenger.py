import cv2  # "opencv-python" from pip
import numpy as np
from PIL import ImageGrab  # "Pillow" from pip
from time import sleep
import pytesseract
import ctypes

from telegram.ext import Updater

# pytesseract executeable from https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# assumes WoW is running under Windows (tested on Win 10 Pro)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

print("screensize: " + str(screensize))

center_x = screensize[0] / 2
center_y = screensize[1] / 2

x_margin = screensize[0] / 12
y_margin = screensize[1] / 12

queue_msg_box = center_x - x_margin, \
                center_y - y_margin, \
                center_x + x_margin, \
                center_y + y_margin


# adapted from sentdex https://www.youtube.com/watch?v=ks4MPfMq8aQ <-- watch that series
while True:
    np_image_grab = np.array(ImageGrab.grab(bbox=queue_msg_box))

    hsv_image = cv2.cvtColor(np_image_grab, cv2.COLOR_BGR2HSV)
    cv2.imshow('preview', hsv_image)

    # character recognition happens HERE
    print(pytesseract.image_to_string(hsv_image))

    if cv2.waitKey(25) and 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    sleep(5)


# telegram bot stuff

