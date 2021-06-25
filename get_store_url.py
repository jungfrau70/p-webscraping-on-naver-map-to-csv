import pandas as pd
import time

from bs4 import BeautifulSoup as bs
from pandas import read_excel
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import trange
from urllib.parse import quote_plus

options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument("window-size=1920x1080") # 가상화면 크기
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")

keywords = ['서울특별시 올리브영']

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)
interval = 4

def download_url(keyword, pnum):

    kword = quote_plus(keyword)
    entry_url = f'https://m.map.naver.com/search2/search.naver?query={kword}&sm=hty&style=v5#/list'

    try:
        # 키워드 지식인 검색
        driver.get(entry_url)
        time.sleep(interval)

        # # Scrap할 페이지 수만큼 열기
        # pages = pnum // 20
        # for i in trange(pages):  # 페이지별 20개 Posts
        #     try:
        #         driver.find_element_by_xpath("//*[@id='moreContainer']/div/a[1]").click()
        #         time.sleep(interval)
        #     except:
        #         continue

        # # 최대 75개 검색결과 제약에 해당하는지 여부 판별
        # try:
        #     ret = driver.find_element_by_xpath('//*[@id="ct"]/div[2]/p[2]')
        # except:
        #     print(ret)

    except:
        print(entry_url)

    soup = bs(driver.page_source, 'html.parser')
    get_details = soup.find_all('a', attrs={"class": "item_thumb _itemThumb"})

    # 온전한 postURL 만들기
    urls = []
    for val in get_details:
        get_val = val["data-cid"]
        url = f'https://m.map.naver.com/search2/site.naver?query={kword}=hty&style=v5&code={get_val}'
        urls.append(url)

    df_postURLs = pd.DataFrame({"url": urls})

    return df_postURLs


# 지식인 키워드 검색 Main 호출
pnum = 10000
for keyword in keywords:
    try:
        df_URL = download_url(keyword, pnum)
        filename = "./" + "URL_" + keyword.replace(" ", "") + ".csv"
        df_URL.to_csv(filename, index=False)
    except:
        continue

driver.close()
driver.quit()


