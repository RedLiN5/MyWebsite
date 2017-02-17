import requests
import urllib
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys


class CollectWeibo(object):

    def __init__(self, max_page, username, password):
        self.max_page = max_page
        self.username = username
        self.password = password

    def trade_spider(self):
        columns = ['Investor', 'Investee', 'Industry', 'Date', 'FinancingRound', 'Amount']
        df = pd.DataFrame(columns = columns)
        page_num = int(1)

        while  page_num <= self.max_page:
            try:
                url = 'https://www.itjuzi.com/investfirm?page=%s'% str(page_num)
                hdr = {'User-Agent': 'Mozilla/5.0'}
                request = urllib.request.Request(url, headers=hdr)
                page = urllib.request.urlopen(request)
                soup = BeautifulSoup(page, "lxml")
                general_data = soup.find_all("ul", {"class": "list-main-investset"})
                data_content = general_data[1].find_all('li')

                for content in data_content:
                    Investor = content.contents[4].text.strip(' ')
                    url = content.contents[4].find_all('a')[0].get('href')

                    USERNAME = self.username
                    PASSWORD = self.password
                    session = requests.Session()

                    login_data = {'identity':USERNAME, 'password':PASSWORD}
                    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                    response = session.get(url, cookies={'from-my': 'browser'}, headers=headers, data=login_data)
                    soup = BeautifulSoup(response.text, 'lxml')

            except:
                print('error')
