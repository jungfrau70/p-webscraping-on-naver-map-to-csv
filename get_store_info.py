# 라이브러리 로드
# requests는 작은 웹브라우저로 웹사이트 내용을 가져온다.
import requests
# BeautifulSoup 을 통해 읽어 온 웹페이지를 파싱한다.
from bs4 import BeautifulSoup as bs

# 크롤링 후 결과를 데이터프레임 형태로 보기 위해 불러온다.
import pandas as pd
import time

# 비동기적으로 콜러블을 실행하는 인터페이스를 제공한다.
import concurrent.futures

MAX_THREADS = 300


def scrape_info(url):

    # 크롤링 할 사이트
    try:
        res = requests.get(url[0], headers=headers)
        # print(res)
        res.raise_for_status()

        time.sleep(4)

        soup = bs(res.text, 'html.parser')

        title = soup.select_one('#_siteviewTopArea > div.search_address > strong').text
        address1 = soup.select_one(
            '#_siteviewTopArea > div.search_address > div.wrap_bx_address2 > div:nth-child(1)').text
        address2 = soup.select_one(
            '#_siteviewTopArea > div.search_address > div.wrap_bx_address2 > div:nth-child(2) > span').text
        open_days = soup.select_one('#_baseInfoTab > div > div > ul > li > strong').text
        open_hours = soup.select_one('#_baseInfoTab > div > div > ul > li > span').text

    except:
        pass

    # (향후) 수집 정보를 보완한 후, 데이터베이스 테이블에 저장한다.
    df = pd.DataFrame(title, address1, address2, open_days, open_hours)
    print(df)
    return df


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


def get_stores(urls):
    threads = min(MAX_THREADS, len(urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future = executor.map(scrape_info, urls)
        print(future.result())


keywords = ['서울특별시 올리브영']

if __name__ == '__main__':

    # 정보 가져오기
    t0 = time.time()

    for keyword in keywords:
        print(keyword)
        filename = "./" + "URL_" + keyword.replace(" ", "") + ".csv"
        print(filename)

        # 파일 읽기
        df_URL = pd.read_csv(filename)
        urls = df_URL.values.tolist()

        try:
            # 파일 쓰기
            df_info = get_stores(urls)
            output_filename = "./" + "STORE_" + keyword.replace(" ", "") + ".csv"
            print(output_filename)
            df_info.to_csv(output_filename, date_format='%Y%m%d', encoding='utf-8-sig')
        except:
            continue

    t1 = time.time()
    print(f"{t1 - t0} seconds to get {len(urls)} stores.")


