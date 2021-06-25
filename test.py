# https://jlim0316.tistory.com/m/2

from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import requests

keywords = ['서울특별시 올리브영']

add_name = []

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


for keyword in keywords:
    print(keyword)
    filename = "./" + "URL_" + keyword.replace(" ", "") + ".csv"
    print(filename)

    # 파일 읽기
    df_URL = pd.read_csv(filename)
    print(df_URL)
    urls = df_URL.values.tolist()

    for url in urls:
        print(url[0])
        res = requests.get(url[0], headers=headers)
        res.raise_for_status()

        time.sleep(4)

        soup = bs(res.text, 'html.parser')

        title = soup.select_one('#_siteviewTopArea > div.search_address > strong').text
        address1 = soup.select_one('#_siteviewTopArea > div.search_address > div.wrap_bx_address2 > div:nth-child(1)').text
        address2 = soup.select_one('#_siteviewTopArea > div.search_address > div.wrap_bx_address2 > div:nth-child(2) > span').text
        open_days = soup.select_one('#_baseInfoTab > div > div > ul > li > strong').text
        open_hours = soup.select_one('#_baseInfoTab > div > div > ul > li > span').text

        print(title)
        print(address1)
        print(address2)
        print(open_days)
        print(open_hours)



    # q = soup.find_all('div strong', attrs={"class": "search_address"}).get_text()