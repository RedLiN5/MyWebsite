# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
url = "http://sz.fang.anjuke.com/loupan/all/p{page}/"

page = 0

csv_file = open("xinfang.csv",'w',newline='',encoding='utf-8-sig')
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text, "lxml")
    house_list = html.select(".key-list > div")

    if not house_list:
        break

    if page >10:
        break

    for house in house_list:
        try:
            house_title = house.select("h3")[0].string
            house_url = urljoin(url, house['data-link'])
            csv_writer.writerow([house_title, house_title, house_url, house_url])
        except Exception as e:
            print("Page:"+str(page))
            print(e)



csv_file.close()
