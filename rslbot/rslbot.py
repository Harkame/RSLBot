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
from enum import Enum

HOME_BUTTON_POPUP = [40, 28, 42]

def set_interval(callback, time, once=False):
    event = threading.Event()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if once:
        callback()  # call once

    while not event.wait(time):
        callback()


def confirm():
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

        print(item_name)
        print(item_name_2)

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

def extract_first_pixel(x, y):
    file_name = "i.png"
    image1 = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))

    #for i in range(397, 597):
    #    image1 = ImageGrab.grab(bbox=(i, 523, i+1, 524))

    image1.save(file_name)
    im = Image.open(file_name)
    pix = im.load()
    return np.asarray(pix[0, 0])

def is_popup_displayed():
    if get_current_position() != Position.HOME:
        return False

    pix = extract_first_pixel(830, 980)

    print(pix)

    return pixel_close(HOME_BUTTON_POPUP, pix, 5)


def close_popup():
    pyautogui.click(420, 980)

def pixel_close(p1, p2, approx):
    for i in range(0, len(p1)):
        if not p1[i] - approx < p2[i] < p1[i] + approx:
            return False

    return True

def get_current_position():
    filename = "i.png"
    image1 = ImageGrab.grab(bbox=(805, 985, 870, 1012))
    image1.save(filename)
    im = Image.open(filename)
    pix = im.load()

    im = cv2.imread(filename)
    word = pytesseract.image_to_string(im).lower()

    if "battle" in word:
        return Position.HOME

    return Position.UNKNOWN

def check_arena():
    print("check_arena")

    base_start_vertical = 97
    vertical_scale = 94
    horizontal_start = 535
    horizontal_end = 747
    case_height = 75

    for index in range(1, 9):
        vertical_start = base_start_vertical + (vertical_scale * index)
        vertical_end = case_height + vertical_start

        file_name = "i" + str(index) + ".png"
        image1 = ImageGrab.grab(
            bbox=(horizontal_start, vertical_start, horizontal_end, vertical_end)
        )
        image1.save(file_name)

        im = Image.open(file_name)
        pix = im.load()

        print(pix[79, 37])

        os.remove(file_name)
        time.sleep(1)

def pixel_close(p1, p2, approx):
    for i in range(0, len(p1)):
        if not p1[i] - approx < p2[i] < p1[i] + approx:
            return False

    return True

def open_shop():
    if get_current_position() == Position.HOME:
        pyautogui.click(200, 800)

def replay():
    filename = "i.png"
    image1 = ImageGrab.grab(bbox=(462, 999, 508, 1015))
    image1.save(filename)
    im = Image.open(filename)
    pix = im.load()

    im = cv2.imread(filename)
    word = pytesseract.image_to_string(im).lower()

    if "replay" in word:
        pyautogui.click(500, 1000)

class Position(Enum):
    UNKNOWN = -1
    HOME = 0

def get_remaining_energy():
    energy = 0
    filename = "i.png"
    image1 = ImageGrab.grab(bbox=(860, 215, 882, 230))
    image1.save(filename)
    im = Image.open(filename)
    pix = im.load()

    im = cv2.imread(filename)
    word = pytesseract.image_to_string(im).lower()

    try:
        energy = int(word.split('\n')[0])
    except:
        print(word)

    return energy

def get_energy_cost():
    cost = 99999
    filename = "i.png"
    image1 = ImageGrab.grab(bbox=(718, 996, 745, 1015))
    image1.save(filename)
    im = Image.open(filename)
    pix = im.load()

    im = cv2.imread(filename)
    word = pytesseract.image_to_string(im)

    try:
        cost = int(word.split('\n')[0])
    except:
        print(word)


    return cost

if __name__ == "__main__":
    """
    while is_popup_displayed():
        close_popup()
        time.sleep(1)
    """
    #open_shop()

    #check_market()

    #replay()
    while(True):
        #if get_remaining_energy() > get_energy_cost():
        replay()

        time.sleep(30)
