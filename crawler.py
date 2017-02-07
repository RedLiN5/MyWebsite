# -*- coding: utf-8 -*-

import time
import re
import codecs
import pandas as pd
from selenium import webdriver
import selenium.webdriver.support.ui as ui


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
            self.driver = webdriver.Firefox()
            self.driver.get('http://weibo.com/')
            elem_user = self.driver.find_element_by_name('username')
            elem_user.send_keys('')
            elem_password = self.driver.find_element_by_name('password')
            elem_password.send_keys('')

            # img = self.driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
            # src = img.get_attribute('src')
            # name = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            # urllib.request.urlretrieve(src, "ValidationImages/" +\
            #                            name +\
            #                            ".jpg")
            #
            # # TODO(Leslie): To recognize validation codes.
            # answer = ocr(im = "ValidationImages/" + name + ".jpg")
            # elem_cap = self.driver.find_element_by_name('code')
            # elem_cap.send_keys(answer)
            # time.sleep(3)

            elem_remem = self.driver.find_element_by_id('login_form_savestate')
            elem_remem.click()
            elem_submit = self.driver.find_element_by_class_name('W_btn_a')
            elem_submit.click()
            time.sleep(2)

        except Exception as e:
            print('Error:', e)
        finally:
            print(u'End LoginWeibo!\n\n')

    def search_user(self, user=None):
        if not user:
            raise ValueError('"user" cannot be empty')

        if user:
            elem_input = self.driver.find_element_by_class_name('gn_search_v2')
            elem_keyword = elem_input.find_element_by_xpath('input')
            elem_keyword.send_keys(user)
            elem_submit = elem_input.find_element_by_xpath('a')
            elem_submit.click()
        else:
            raise ValueError('"user" cannot be empty')

        try:
            elem_star = self.driver.find_element_by_class_name('star_detail')
            elem_star.find_element_by_class_name('name_txt').click()
        except:
            raise ('Cannot find the user')

        windows = self.driver.window_handles
        # Close last tab
        self.driver.switch_to.window(windows[0])
        self.driver.close()
        self.driver.switch_to.window(windows[1])

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
        # WAP website can only show 200 followings
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
                # TODO Count number of tag 'table'
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
        # windows = self.driver.window_handles
        # if len(windows) == 1:
        #     new_window = self.driver.window_handles[-1]
        #     self.driver.switch_to.window(new_window)
        # elif len(windows) > 1:
        #     current_window = self.driver.current_window_handle
        #     current_window_pos = [i for i, x in enumerate(windows)
        #                           if x == current_window]
        #     new_window = windows[current_window_pos + 1]
        #     self.driver.switch_to.window(new_window)

        elem_likes = self.driver.find_element_by_class_name('PCD_pictext_f')
        elem_likes.find_element_by_class_name('more_txt').click()
        elem_likeswb = self.driver.find_element_by_id('Pl_Core_LikesFeedV6__68')
        elem_all_likes_wb = elem_likeswb.find_element_by_class_name('WB_feed')
        all_likes_wb = elem_all_likes_wb.find_elements_by_xpath('div')

        deletes = 0
        for element in all_likes_wb:
            class_name = element.find_element_by_xpath('div[1]').get_attribute('class')
            if class_name == 'WB_empty':
                deletes += 1
            #elif

        #test.send_keys(Keys.COMMAND + Keys.ENTER)


        #like_part = self.driver.find_element_by_id('Pl_Official_LikeMerge__16')


    def _quit(self):
        elem_setting = self.driver.find_element_by_class_name('W_ficon')
        elem_setting.click()