# -*- coding: utf-8 -*-

from selenium import webdriver
import pyautogui
from PIL import Image
from password import password_type
from captcha import CaptchaResolver
import sys, json, time, traceback

reload(sys)
sys.setdefaultencoding('utf-8')

iedriver = "bin\IEDriverServer_Win32_3.9.0.exe"
timestamp = str(int(round(time.time() * 1000)))
screenshot_img = 'tmp/screenshot_' + timestamp + '.png'
browser = None

def home():
    global browser
    browser = webdriver.Ie(iedriver)
    browser.get("https://pay.sc.189.cn/#/login")
    browser.maximize_window()


def login(username, password):
    try:
        home()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)

    #browser.quit()
    return


if __name__ == '__main__':
    login("test123", "test123")

#End
