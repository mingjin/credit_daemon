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
screenshot_img = 'screenshot_' + timestamp + '.png'
browser = None

def home():
    global browser
    browser = webdriver.Ie(iedriver)
    browser.get("https://ipcrs.pbccrc.org.cn/")
    browser.maximize_window()

def refresh():
    browser.find_element_by_class_name('yzm_a').click()

def jump_to_login_page():
    browser.switch_to.frame("conFrame")
    browser.find_element_by_css_selector("a.startBtn").click()

    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    
def get_captcha():
    browser.save_screenshot(screenshot_img)
    result = CaptchaResolver().resolve_captcha(screenshot_img)
    print screenshot_img + ":  " + result
    return result
        
def submit_login_form(username, password):
    browser.switch_to.frame("conFrame")
    browser.find_element_by_id("loginname").send_keys(username)

    pyautogui.click(215, 400)
    password_type(password)
        
    captcha = get_captcha()
    browser.find_element_by_id("_@IMGRC@_").send_keys(captcha)

    time.sleep(1)
    #browser.find_element_by_css_selector("form[name='loginForm'] input[type='submit']").click()

def login(username, password):
    try:
        home()
        jump_to_login_page()
        submit_login_form(username, password)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)

    #status: -1表示验证码错误，0表示登录名或密码错误，1表示登录成功，-2表示未知错误
    status = 0
    result = ''
    errMsg = ''
    _msg_ = ''
    lgnInfo = ''
    pwdInfo = ''
    
    try:
        lgnInfo = browser.find_element_by_id('loginNameInfo').text
        pwdInfo = browser.find_element_by_id('passwordInfo').text
        print('loginNameInfo:%s, passwordInfo:%s' %(lgnInfo, pwdInfo))
    except:
        print('loginNameInfo or passwordInfo not exist!')
        
    try:
        errMsg = browser.find_element_by_id('_error_field_').text
    except:
        print('errMsg not exist!')
    
    try:
        _msg_ = browser.find_element_by_id('_@MSG@_').text
    except:
        print('_msg_ not exist!')
        
    print('errorMsg:' + errMsg)
    print('_msg_:' + _msg_)
    
    msg = errMsg if errMsg != '' else _msg_ 
    inputInfo = lgnInfo if lgnInfo != '' else pwdInfo
    print('msg=' + msg)
    if len(msg.strip()) > 0:
        if '验证码输入错误' in msg:
            status = -1
        elif '登录名或密码错误' in msg:
            status = 0
        else:
            status = -2
    elif len(inputInfo.strip()) > 0:
        status = -3
        msg = '登录名或密码输入错误，请重试!'
    else:
        status = 1
        msg = '登录成功'
        result = ';'.join([item['name'] + '=' + item['value'] for item in browser.get_cookies()])

    browser.quit()
    ret = {}
    ret['result'] = result
    ret['status'] = status
    ret['message'] = msg
    return json.dumps(ret, ensure_ascii=False)


login("test123", "test123")
