# -*- coding: utf-8 -*-

import time
import re
import os
import sys
import datetime
import codecs
import pandas as pd
import shutil
import urllib.request
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pyocr import ocr
# from validate import *


#全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info.txt", 'a', 'utf-8')

class SinaWeibo(object):

    def __init__(self):
        self.driver = webdriver.Firefox()
        wait = ui.WebDriverWait(self.driver, 10)
        self.df = pd.DataFrame(columns=['ID', 'UserName'])

    def login(self, username, password):
        try:
            self.driver.get("http://login.weibo.cn/login/")
            elem_user = self.driver.find_element_by_name("mobile")
            elem_user.send_keys(username)  # 用户名
            elem_pwd = self.driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
            elem_pwd.send_keys(password)  # 密码

            img = self.driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
            src = img.get_attribute('src')
            name = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            urllib.request.urlretrieve(src, "ValidationImages/" +\
                                       name +\
                                       ".jpg")

            # TODO(Leslie): To recognize validation codes.
            answer = ocr(im = "ValidationImages/" + name + ".jpg")
            elem_cap = self.driver.find_element_by_name('code')
            elem_cap.send_keys(answer)
            time.sleep(3)

            elem_remem = self.driver.find_element_by_name('remember')
            elem_remem.click()
            elem_sub = self.driver.find_element_by_name("submit")
            elem_sub.click()  # 点击登陆
            time.sleep(2)

        except Exception as e:
            print('Error:', e)
        finally:
            print(u'End LoginWeibo!\n\n')

    def search_user(self, user=None):
        if not user:
            raise ValueError('"user" cannot be empty')
        elem_search = self.driver.find_element_by_xpath('html/body/div[2]/a[4]')
        elem_search.click()
        elem_keyword = self.driver.find_element_by_name('keyword')

        if user:
            elem_keyword.send_keys(user)
            elem_submit = self.driver.find_element_by_name('suser')
            elem_submit.click()
        else:
            raise ValueError('"user" cannot be empty')

        elem_user = self.driver.find_element_by_xpath('html/body/table[1]/tbody/tr/td[2]/a')
        elem_user.click()

    def search_weibo(self, weibo=None):
        if not weibo:
            raise ValueError('"weibo" cannot be empty')
        elem_search = self.driver.find_element_by_xpath('html/body/div[2]/a[4]')
        elem_search.click()
        elem_keyword = self.driver.find_element_by_name('keyword')

        if weibo:
            elem_keyword.send_keys(weibo)
            elem_submit = self.driver.find_element_by_name('smblog')
            elem_submit.click()
        else:
            raise ValueError('"weibo" cannot be empty')

    def _following(self):
        ids = []
        usernames = []
        elem_following = self.driver.find_element_by_xpath('html/body/div[2]/div/a[1]')
        elem_following.click()
        elem_pagelist = self.driver.find_element_by_id('pagelist')
        pagelist = elem_pagelist.find_element_by_tag_name('div').text
        m = re.search("/([0-9]+)页", pagelist)
        total_page = int(m.group(1))

        for i in range(total_page):
            for j in range(10):
                elem_user = self.driver.find_element_by_xpath('html/body/table[%d]'%(j+1))
                elem_user_url = elem_user.find_element_by_xpath('table/tbody/tr/td[2]/a')
                username = elem_user_url.text
                url = elem_user_url.get_attribute('href')
                m = re.search('/([0-9]+)\?', url)
                id = m.group(1)
                ids.append(id)
                usernames.append(username)

    def _friend(self):
        pass

    def _sort_by_likes(self):
        pass