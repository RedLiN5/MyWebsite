# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import bs4
from time import localtime, strftime
import random
import string

class DoubanRent(object):

    def __init__(self, username=None, password=None,
              urls=None, max_page=50, keywords=None):
        self.username = username
        self.password = password
        self.urls = urls
        self.max_page = max_page
        self.keywords = keywords

    def start(self):
        current_time = strftime("%Y-%m-%d_%H:%M:%S", localtime())
        if self.username is None or self.password is None:
            raise ValueError('"username" or "password" may not be valid')

        if self.urls is None:
            raise ValueError('"urls" cannot be empty')

        if self.keywords is None:
            raise ValueError('"keywords" cannot be empty')

        if isinstance(self.urls, list):
            for url in self.urls:
                df, name = self._crawler(urlfront=url)
                df.to_csv(name+current_time+'.csv',
                          index=False,
                          encoding='utf_8')
        elif isinstance(self.urls, str):
            url = self.urls
            df, name = self._crawler(urlfront=url)
            df.to_csv(name+current_time+'.csv',
                      index=False,
                      encoding='utf_8')
        print('Congratulations! Crawler is finished successfully!')

    def _crawler(self, urlfront):
        columns = ['url', 'title', 'response_num']
        urls = []
        titles = []
        responses = []
        index = 0
        r = requests.Session()
        payload = {'form_email': self.username, 'form_password': self.password}
        p = r.post('https://www.douban.com/', data=payload)
        cookie = {'Cookie': ''}
        if p.status_code == 200:
            cookie_dict = p.cookies.get_dict()
            cookie_item = [name + '=' + cookie_dict[name] for name in cookie_dict if name != 'bid']
            cookie = {'Cookie': '; '.join(cookie_item)}
        url_temp = urlfront + 'discussion?start=' + str(0)
        page = requests.get(url_temp)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        text = soup.findAll('div', 'title')[0].text
        group_name = text.strip('\n')

        for page in range(self.max_page):
            page_index = page*25
            url = urlfront + 'discussion?start=' + str(page_index)
            headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) "+
                                     "Gecko/20100101 Firefox/51.0"}
            cookie['Cookie'] = cookie['Cookie'] + '; bid=' \
                               + "".join(random.sample(string.ascii_letters + string.digits, 11))

            page = requests.get(url, headers=headers,
                                cookies=cookie,
                                timeout=(6.1, 5))
            soup = bs4.BeautifulSoup(page.text, 'html5lib')
            items = soup.findAll('td', 'title')
            for item in items:
                target = item.find('a')
                href = target.attrs['href']
                response = item.find_parent().findAll('td')[2].text
                title = target.attrs['title']
                if any(s in title for s in self.keywords):
                    urls.append(href)
                    titles.append(title)
                    responses.append(response)
                    index += 1
        df = pd.DataFrame(data=np.array([urls, titles, responses]).T,
                                        columns=columns)
        return df, group_name


