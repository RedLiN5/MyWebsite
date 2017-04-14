# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import datetime
import pandas as pd
import numpy as np
import glob
import os
import sys
import time
import json
from pymongo import MongoClient
from time import localtime, strftime
from selenium import webdriver


class CollectWeibo(object):

    def __init__(self, max_page=50, bloger=None):
        self.max_page = max_page
        self.bloger = bloger
        self._get_captcha()

    def _get_captcha(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://weibo.cn/login/')
        item = self.driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
        url_captcha = item.get_attribute('src')
        image_captcha = requests.get(url_captcha)
        current_time = strftime("%Y%m%d_%H%M%S", localtime())
        self.captcha_name = 'captcha_{0}.jpg'.format(current_time)
        open('static/login_captcha/'+self.captcha_name, 'wb').write(image_captcha.content)

    def get_cookie(self, captcha=None):
        elem_user = self.driver.find_element_by_name('mobile')
        elem_user.clear()
        elem_user.send_keys('13652063773')
        elem_password = self.driver.find_element_by_name('password_2791')
        elem_password.send_keys('4372125')
        elem_captcha = self.driver.find_element_by_name('code')
        elem_captcha.send_keys(captcha)
        elem_remem = self.driver.find_element_by_name('remember')
        elem_remem.click()
        time.sleep(1)
        cookie = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
        mycookie = {'Cookie': '; '.join(cookie)}
        self.driver.quit()
        return mycookie

    def get_weibo(self, cookie=None, bloger_page=None, nickname=None):
        if len(cookie['Cookie'])>1:
            self.mycookie = cookie
        else:
            raise ValueError('"Cookie" cannot be empty')
        m = re.search("/([a-z0-9]+)\?", bloger_page)
        user_id = m.group(1)
        url_front = 'http://weibo.cn/%s?page=' % (user_id)
        columns = ['Date', 'Like', 'Repost', 'Comment']
        # Type includes 'only text', 'photo', 'video' and 'repost'
        page_num = int(1)
        pub_dates =[]
        likes = []
        reposts = []
        comments = []
        print('start weibo collecting')

        while page_num <= self.max_page:
            url = url_front + str(page_num)
            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) " +
                                     "Gecko/20100101 Firefox/51.0"}
            html = requests.get(url,
                                cookies=self.mycookie,
                                headers=headers)
            selector = etree.HTML(html.content)
            items = selector.xpath("//div[@class='c' and @id]")
            num_item = len(items)
            if num_item > 1:
                for i in range(num_item):
                    item = items[i]
                    info = item.xpath("div/a[@href]")[-4:]
                    pub_info = item.xpath("div/span[@class='ct']")[-1]
                    try:
                        m1 = re.search("赞\[([0-9]+)\]",
                                       info[0].text)
                        m2 = re.search("转发\[([0-9]+)\]",
                                       info[1].text)
                        m3 = re.search("评论\[([0-9]+)\]",
                                       info[2].text)
                        like = m1.group(1)
                        repost = m2.group(1)
                        comment = m3.group(1)
                        pub_time = pub_info.text
                        # '今天 10:05\xa0来自胖哥杨力的iPhone 7 Plus'
                        likes.append(like)
                        reposts.append(repost)
                        comments.append(comment)
                        if re.search('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', pub_time):
                            m = re.search('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}', pub_time)
                            pub_dates.append(m.group(0))
                        elif '今天' in pub_time:
                            date = datetime.datetime.now().strftime("%Y-%m-%d")
                            pub_dates.append(date)
                        elif re.search('([0-9]{1,2})月([0-9]{1,2})日', pub_time):
                            month, day = re.search('([0-9]{1,2})月([0-9]{1,2})日',
                                                   pub_time).group(1, 2)
                            year = datetime.datetime.now().strftime("%Y")
                            date = '{0}-{1}-{2}'.format(year, month, day)
                            pub_dates.append(date)
                        print('Finish crawling page {0}'.format(page_num))
                    except Exception as e:
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, 'line ', exc_tb.tb_lineno)

            page_num += 1

        self.df = pd.DataFrame(data = np.array([pub_dates, likes, reposts, comments]).T,
                               columns = columns)
        self.nickname = nickname
        file_name = '{0}_weibos.csv'.format(nickname)
        exist_files = glob.glob('static/data/*.csv')
        if any(file_name in file for file in exist_files):
            os.remove('static/data/'+file_name)
        self.df.to_csv('static/data/'+file_name, sep=',',
                  encoding='utf-8')

    def _to_mongodb(self):
        try:
            client = MongoClient('localhost', 27017)
            db = client['weibo']
            records = json.loads(self.df.T.to_json()).values()
            eval('db.' + self.nickname + '_weibos.insert_many(records)')
        except Exception as e:
            print('Weibo data cannot save to Mongodb for the following reason:', e)