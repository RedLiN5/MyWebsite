# -*- coding: utf-8 -*-

import requests
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
from likes_collect import CollectLikes


class CollectWeibo(CollectLikes):

    def __init__(self, max_page=None, cookie=None):
        super(CollectLikes, self).__init__()
        self.max_page = max_page
        session = requests.Session()
        login_url = "https://passport.weibo.cn/signin/login"
        login_data = {'loginName': self.username, 'loginPassword': self.password}
        r = session.post(login_url, data=login_data)

    def trade_spider(self):
        columns = ['Time', 'Type']
        # Type includes 'only text', 'photo', 'video' and 'repost'
        df = pd.DataFrame(columns = columns)
        page_num = int(1)

        while page_num <= self.max_page:
            try:
                


            except Exception as e:
                print(e)
