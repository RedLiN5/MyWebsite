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
from likes_collect import CollectLikes
from pymongo import MongoClient

class CollectWeibo(object):

    def __init__(self, max_page=50, bloger=None):
        self.max_page = max_page
        self.bloger = bloger

    def get_weibo(self, cookie=None, bloger_page=None, nickname=None):
        if len(cookie['Cookie'])>1:
            self.mycookie = cookie
        else:
            raise ValueError('"cookie" cannot be empty')
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

        while page_num <= self.max_page:
            url = url_front + str(page_num)
            html = requests.get(url, cookies=self.mycookie).content
            selector = etree.HTML(html)
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

                    except Exception as e:
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, 'line ', exc_tb.tb_lineno)

            page_num += 1

        print(np.array([pub_dates, likes, reposts, comments]).shape)
        self.df = pd.DataFrame(data = np.array([pub_dates, likes, reposts, comments]).T,
                               columns = columns)
        self.nickname = nickname
        file_name = '{0}_weibos.csv'.format(nickname)
        exist_files = glob.glob('data/*.csv')
        if file_name in exist_files:
            os.remove('data/'+file_name)
        self.df.to_csv('data/'+file_name, sep=',',
                  encoding='utf-8')

    def _to_mongodb(self):
        client = MongoClient('localhost', 27017)
        db = client['weibo']
        collection = eval('db.'+self.nickname+'_weibos')
        collection.insert_many(self.df.to_dict('records'))
