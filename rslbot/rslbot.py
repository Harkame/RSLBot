import pyscreenshot as ImageGrab
import cv2
import pytesseract
from pynput.mouse import Button, Controller
from PIL import Image
import threading
import signal
import time
import sys
import pyautogui
import numpy as np
from PIL import Image
from win32api import GetSystemMetrics
import os
import pygetwindow as gw
from win32api import GetMonitorInfo, MonitorFromPoint
import numpy

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)


def set_interval(callback, time, once=False):
    event = threading.Event()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if once:
        callback()  # call once

    while not event.wait(time):
        callback()


def confirm():
    if width == 2560 and height == 1440:
        pyautogui.click(800, 830)
    else:
        pyautogui.click(600, 620)


def check_item(x, y):
    pass


def check_market():
    print("Check market")

    vertical_scale = 100
    horizontal_start = 110
    horizontal_end = 250
    horizontal_start_2 = 460
    horizontal_end_2 = 620
    case_height = 60

    if width == 2560 and height == 1440:
        vertical_scale = 130
        horizontal_start = 145
        horizontal_end = 345
        horizontal_start_2 = 620
        horizontal_end_2 = 820
        case_height = 75

    for index in range(1, 7):

        vertical_start = vertical_scale * index
        vertical_end = case_height + vertical_start

        file_name = "i" + str(index) + ".png"
        file_name_2 = "i" + str(index) + "b.png"

        image1 = ImageGrab.grab(
            bbox=(horizontal_start, vertical_start, horizontal_end, vertical_end)
        )
        image1.save(file_name)

        image2 = ImageGrab.grab(
            bbox=(horizontal_start_2, vertical_start, horizontal_end_2, vertical_end)
        )
        image2.save(file_name_2)

        image_read = cv2.imread(file_name)
        item_name = pytesseract.image_to_string(image_read, lang="num",).lower()

        image_read_2 = cv2.imread(file_name_2)
        item_name_2 = pytesseract.image_to_string(image_read_2, lang="num",).lower()

        if "shard" in item_name:
            pyautogui.click(horizontal_start, vertical_start)
            time.sleep(1)
            confirm()

        if "shard" in item_name_2:
            pyautogui.click(horizontal_start_2, vertical_start)
            time.sleep(1)
            confirm()

        os.remove(file_name)
        os.remove(file_name_2)


def resize():

    global width
    global height

    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    taskbar_height = int(monitor_area[3] - work_area[3])

    window = gw.getWindowsWithTitle("Raid: Shadow Legends")[0]

    window.activate()

    window.resizeTo(int(width / 2), int(height - taskbar_height))
    window.moveTo(0, 0)


def is_popup_displayed():
    image1 = ImageGrab.grab(bbox=(900, 1200, 901, 1201))
    image1.save("popup.png")
    im = Image.open("popup.png")
    pix = im.load()

    return pix[0, 0][0] < 50 and pix[0, 0][1] < 65 and pix[0, 0][2] < 75


def close_popup():
    pyautogui.click(900, 1200)


def get_current_position():
    pass


def run(argv):
    global width
    global height

    if len(argv) > 1:
        width = int(argv[1])
        height = int(argv[2])

    # resize()

    while is_popup_displayed():
        close_popup()
        time.sleep(2)

    check_market()

    # set_interval(check_market, 5)


if __name__ == "__main__":
    run(sys.argv)
