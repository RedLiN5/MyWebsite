# -*- coding: utf-8 -*-

import time
import re
import os
import sys
import datetime
import codecs
import shutil
import urllib.request
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pyocr import ocr
# from validate import *

driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,10)

#全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info.txt", 'a', 'utf-8')


def LoginWeibo(username, password):
    try:
        driver.get("http://login.weibo.cn/login/")
        elem_user = driver.find_element_by_name("mobile")
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
        elem_pwd.send_keys(password)  # 密码

        img = driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
        src = img.get_attribute('src')
        name = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        urllib.request.urlretrieve(src, "ValidationImages/" +\
                                   name +\
                                   ".jpg")

        # TODO(Leslie): To recognize validation codes.
        answer = ocr(im = "ValidationImages/" + name + ".jpg")
        elem_cap = driver.find_element_by_class_name('code')
        elem_cap.send_keys(answer)

        time.sleep(5)

        elem_sub = driver.find_element_by_name("submit")
        elem_sub.click()  # 点击登陆
        time.sleep(2)

    except Exception as e:
        print('Error:', e)
    finally:
        print(u'End LoginWeibo!\n\n')

def RetrieveData():
    pass

def SaveDataset():
    pass


if __name__ == '__main__':
    LoginWeibo(username='13652063773',
               password='4372125')