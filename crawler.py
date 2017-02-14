# -*- coding: utf-8 -*-

import time
import datetime
import re
import codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains



#全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info.txt", 'a', 'utf-8')

class SinaWeibo(object):

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.df = pd.DataFrame(columns=['Bloger', 'PostTime', 'URL'])

    def login(self, username, password):
        try:
            self.driver.get('http://weibo.com/')
            time.sleep(10)
            elem_user = self.driver.find_element_by_name('username')
            elem_user.clear()
            elem_user.send_keys(username)
            elem_password = self.driver.find_element_by_name('password')
            elem_password.send_keys(password)

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

    def search_bloger(self, bloger=None):
        self.bloger = bloger
        if not bloger:
            raise ValueError('"user" cannot be empty')

        if bloger:
            print("Start searching user")
            elem_input = self.driver.find_element_by_class_name('gn_search_v2')
            elem_keyword = elem_input.find_element_by_xpath('input')
            elem_submit = elem_input.find_element_by_xpath('a')
            time.sleep(3)
            elem_keyword.send_keys(bloger)
            elem_submit.click()
            print('Move to bloger search')
            head_menu = self.driver.find_element_by_class_name('search_head_formbox')
            search_user = head_menu.find_element_by_xpath('ul/li/a[2]')
            search_user.click()
        else:
            raise ValueError('"user" cannot be empty')


        time.sleep(5)
        try:
            elem_user_list = self.driver.find_element_by_class_name('pl_personlist')
            most_possible = elem_user_list.find_element_by_xpath('div[1]/div[3]/p/a/em')
            most_possible.click()
        except:
            raise ('Cannot find the user')

        time.sleep(2)
        windows = self.driver.window_handles
        # Close last tab
        self.driver.switch_to.window(windows[0])
        self.driver.close()
        self.driver.switch_to.window(windows[1])

        self._sort_by_likes()

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
        print("Bloger's homepage")
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

        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        elem_likeswb = self.driver.find_element_by_class_name('WB_frame_c')
        elem_all_likes_wb = elem_likeswb.find_element_by_class_name('WB_feed')
        all_likes_wb = elem_all_likes_wb.find_elements_by_xpath('div')

        deletes = 0
        blogers = []
        homepages = []
        visittime = []

        page_str = all_likes_wb[-1].text

        while '下一页' in page_str:
            # Scroll down to bottom of a page
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            elem_likeswb = self.driver.find_element_by_class_name('WB_frame_c')
            elem_all_likes_wb = elem_likeswb.find_element_by_class_name('WB_feed')
            all_likes_wb = elem_all_likes_wb.find_elements_by_xpath('div')

            print('Collecting data')
            for element in all_likes_wb[:-1]:
                class_name = element.find_element_by_xpath('div[1]').get_attribute('class')
                if class_name == 'WB_empty':
                    deletes += 1
                else:
                    wb_info = element.find_element_by_class_name('WB_info')
                    info = wb_info.find_element_by_xpath('a')
                    bloger = info.get_attribute('nick-name')
                    page = info.get_attribute('href')
                    blogers.append(bloger)
                    homepages.append(page)
                    pub_time = element.find_element_by_class_name('WB_from').text
                    if re.search('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', pub_time):
                        m = re.search('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', pub_time)
                        visittime.append(m.group(0))
                    elif '今天' in pub_time:
                        date = datetime.datetime.now().strftime("%Y-%m-%d")
                        visittime.append(date)
                    elif re.search('([0-9]{1,2})月([0-9]{1,2})日', pub_time):
                        month, day = re.search('([0-9]{1,2})月([0-9]{1,2})日',
                                               pub_time).group(1,2)
                        year = datetime.datetime.now().strftime("%Y")
                        date = '{0}-{1}-{2}'.format(year, month, day)
                        visittime.append(date)

            page_str = all_likes_wb[-1].text

            if '下一页' in page_str:
                all_likes_wb[-1].find_element_by_xpath('div/a').click()

        if len(blogers) == len(homepages) == len(visittime):
            self.df['Bloger'] = blogers
            self.df['PostTime'] = visittime
            self.df['URL'] = homepages
        else:
            raise Exception('Lengths of "blogers", "homepages" and "time" are not same.')

        self._quit()
        self.df.to_csv('Friends/{0}_likes.csv'.format(self.bloger),
                       encoding='utf-8')
        #test.send_keys(Keys.COMMAND + Keys.ENTER)


    def _quit(self):
        try:
            top_menu = self.driver.find_elements_by_class_name('gn_set_list')
            setting = top_menu[1]
            ActionChains(self.driver).move_to_element(setting).perform()
            click_quit = setting.find_element_by_xpath('div/ul/li[9]')
            click_quit.click()
        except Exception as e:
            print('Error:', e)
        self.driver.quit()