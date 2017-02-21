# -*- coding: utf-8 -*-

import requests
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import etree
import re
import time
import pandas as pd
import sys
from likes_collect import CollectLikes


class CollectWeibo(CollectLikes):

    def __init__(self, max_page=None):
        super(CollectLikes, self).__init__()
        self.max_page = max_page
        session = requests.Session()
        login_url = "https://passport.weibo.cn/signin/login"
        get_url = "http://weibo.cn/"
        login_data = {'loginName': self.username, 'loginPassword': self.password}
        r = session.post(login_url, data=login_data)
        resp = session.get(get_url)
        d = list(session.cookies.get_dict().items())[0]
        self.mycookie = {'Cookie': d[0] + ':' + d[1]}

    def get_weibo(self):
        m = re.search("/([a-z0-9]+)\?", self.bloger_homepage)
        user_id = m.group(1)
        url_front = 'http://weibo.cn/%d?page=' % (user_id)
        columns = ['Time', 'Type']
        # Type includes 'only text', 'photo', 'video' and 'repost'
        df = pd.DataFrame(columns = columns)
        page_num = int(1)

        while page_num <= self.max_page:
            url = url_front + str(page_num)
            html = requests.get(url, cookies=self.mycookie).content
            selector = etree.HTML(html)
            items = selector.xpath("//div[@class='c']")
            num_item = len(items)
            if num_item > 3:
                for i in range(num_item):
                    item = items[i]
                    info = item.xpath("div/a")






            page_num += 1


            # except Exception as e:
            #     print(e)
