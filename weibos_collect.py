# -*- coding: utf-8 -*-

import requests
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import etree
import re
import time
import datetime
import pandas as pd
import numpy as np
import glob
import os
import sys
from likes_collect import CollectLikes


class CollectWeibo(CollectLikes):

    def __init__(self, max_page=None):
        super(CollectLikes, self).__init__()
        self.max_page = max_page
        self.session = requests.Session()
        login_url = "https://passport.weibo.cn/signin/login"
        login_data = {'loginName': self.username, 'loginPassword': self.password}
        r = self.session.post(login_url, data=login_data)
        self.mycookie = {'Cookie': "SCF=AgtJ6pMqTyS7u12WKayQXv_VFZGcDVVO_7HYTuMX6ACwwIYp7ap0x5ovMiEC1J8GthL08KjyL_ymUS4WEFSCFH4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5q0efpquglaB-ZV4xVgDQ-5JpX5o2p5NHD95QE1K.XSo.Neh-7Ws4DqcjTKsH0dsLLPfv9qgRt; _T_WM=b395d1dd6157cb28a2817c7a240b2ef0; SUB=_2A251qDw5DeRxGeRH4lYX-SnMzjyIHXVXU0RxrDV6PUJbkdBeLXf7kW1jKLcuT_PZ8pK_yatHSUoJdUL26A..; SUHB=0RyaarKRUajzb4; SSOLoginState=1487686761; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"}

    def get_weibo(self):
        m = re.search("/([a-z0-9]+)\?", self.bloger_homepage)
        user_id = m.group(1)
        url_front = 'http://weibo.cn/%d?page=' % (user_id)
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

            page_num += 1
        df = pd.DataFrame(data = np.array([pub_dates, likes, reposts, comments]),
                          columns = columns)
        file_name = '{0}_weibos.csv'.format(self.bloger)
        exist_files = glob.glob('data/*.csv')
        if file_name in exist_files:
            os.remove('data/'+file_name)
        df.to_csv('data/'+file_name, sep=',',
                  encoding='utf-8')
