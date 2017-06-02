# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
url = "http://sz.58.com/ershoufang/pn{page}/"

page = 0

csv_file = open("ershou.csv",'w',newline='',encoding='utf-8-sig')
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text, "lxml")
    house_list = html.select(".house-list-wrap > li")

    if not house_list:
        break

    if page >10:
        break

    for house in house_list:
        house_title = house.select("a")[2].string
        house_url = urljoin(url, house.select("a")[0]["href"])


        house_money = (house.select(".sum")[0].select("b")[0].string + '万')
        csv_writer.writerow([house_title, house_title, house_money, house_url])

csv_file.close()
