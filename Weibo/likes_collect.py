# -*- coding: utf-8 -*-

import time
import datetime
import re
import os
import glob
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import requests
import bs4

class CollectLikes(object):

    def __init__(self, bloger=None):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.df = pd.DataFrame(columns=['Bloger', 'PostTime', 'URL'])
        self.username = '13652063773'
        self.password = '4372125'
        self.bloger = bloger

    def login(self):
        if self.username is None:
            raise ValueError('"username" cannot be empty')
        if self.password is None:
            raise ValueError('"password" cannot be empty')


        try:
            self.driver.get('http://weibo.com/')
            time.sleep(10)
            elem_user = self.driver.find_element_by_name('username')
            elem_user.clear()
            elem_user.send_keys(self.username)
            elem_password = self.driver.find_element_by_name('password')
            elem_password.send_keys(self.password)

            elem_remem = self.driver.find_element_by_id('login_form_savestate')
            elem_remem.click()
            elem_submit = self.driver.find_element_by_class_name('W_btn_a')
            elem_submit.click()
            time.sleep(2)
            cookie = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
            self.mycookie = {'Cookie': '; '.join(cookie)}

        except Exception as e:
            print('Error:', e)

# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---
    def collect_weibo_likes(self):
        cookie = self.mycookie
        url = 'http://weibo.com'
        headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) " +
                                 "Gecko/20100101 Firefox/51.0"}
        html = requests.get(url, cookies=cookie,
                            headers=headers)
        soup = bs4.BeautifulSoup(html.content, 'html5lib')



    def get_likes(self):
        if not self.bloger:
            raise ValueError('"user" cannot be empty')

        if self.bloger:
            print("Start searching user")
            elem_input = self.driver.find_element_by_class_name('gn_search_v2')
            elem_keyword = elem_input.find_element_by_xpath('input')
            elem_submit = elem_input.find_element_by_xpath('a')
            time.sleep(3)
            elem_keyword.send_keys(self.bloger)
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
            most_possible = elem_user_list.find_element_by_xpath('div[1]/div[3]/p/a')
            self.nickname = most_possible.get_attribute('title')
            to_click = most_possible.find_element_by_xpath('em')
            to_click.click()
        except:
            raise ('Cannot find the user')

        time.sleep(2)
        windows = self.driver.window_handles
        # Close last tab
        self.driver.switch_to.window(windows[0])
        self.driver.close()
        self.driver.switch_to.window(windows[1])

        self._sort_by_likes()

    def _sort_by_likes(self):
        print("Move to bloger's likes")
        self.bloger_page = self.driver.current_url
        try:
            elem_likes = self.driver.find_element_by_class_name('PCD_pictext_f')
            elem_likes.find_element_by_class_name('more_txt').click()
            time.sleep(2)
            more_likes = self.driver.find_element_by_xpath("//ul[@class='lev_list']")
            more_likes.find_element_by_xpath('li[3]/a/span').click()

            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            elem_likeswb = self.driver.find_element_by_class_name('WB_frame_c')
            elem_all_likes_wb = elem_likeswb.find_element_by_class_name('WB_feed')
            all_likes_wb = elem_all_likes_wb.find_elements_by_xpath('div')

            deletes = 0
            blogers = []
            homepages = []
            visittime = []

            page_str = all_likes_wb[-1].text
            current_page = 1

            while '下一页' in page_str:
                # Scroll down to bottom of a page
                for _ in range(4):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

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
                print("Finished crawling page %d" % (current_page))

                if '下一页' in page_str:
                    if current_page == 1:
                        all_likes_wb[-1].find_element_by_xpath('div/a').click()
                    elif current_page >10:
                        break
                    else:
                        all_likes_wb[-1].find_element_by_xpath('div/a[2]').click()

                current_page += 1

            if len(blogers) == len(homepages) == len(visittime):
                self.df['Bloger'] = blogers
                self.df['PostTime'] = visittime
                self.df['URL'] = homepages
            else:
                raise Exception('Lengths of "blogers", "homepages" and "time" are not same.')

            self._quit()
            file_name = '{0}_likes.csv'.format(self.nickname)
            exist_files = glob.glob('static/data/*.csv')
            if file_name in exist_files:
                os.remove('static/data/'+file_name)
            self.df.to_csv('static/data/'+file_name, sep=',',
                           encoding='utf-8')
            self._to_mongodb()
        except Exception as e:
            print('This bloger has no thumbs up. Or process encounters following errors:', e)
            self.driver.quit()

    def _to_mongodb(self):
        client = MongoClient('localhost', 27017)
        db = client['weibo']
        records = json.loads(self.df.T.to_json()).values()
        eval('db.' + self.nickname + '_likes.insert_many(records)')

    def _quit(self):
        try:
            setting = self.driver.find_element_by_xpath('//*[@id="pl_common_top"]/div/div/div[3]/div[2]/div[2]/a/em')
            click_quit = self.driver.find_element_by_xpath('//*[@id="pl_common_top"]/div/div/div[3]/div[2]/div[2]/div/ul/li[10]/a')
            actions = ActionChains(self.driver)
            actions.move_to_element(setting)
            actions.click(click_quit)
            actions.perform()
        except Exception as e:
            print('Error:', 'Quit button cannot be found.', '\n', e)
        self.driver.quit()

    def get_homepage(self):
        return self.bloger_page