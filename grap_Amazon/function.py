# function
import re
import time
from selenium import webdriver
from  selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import logging
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 设置日志
logging.basicConfig(level=logging.INFO)

def fetch_website(url, num_pages=1):
    # 初始化
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    data = []

    try:
        for _ in range(num_pages):
            # 打开网页
            driver.get(url)

            # 滚动页面
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # 滚动到底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # 等待页面加载
                time.sleep(3)

                # 计算新的滚动
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            html_content = driver.page_source
            current_page_data = parse_html(html_content)
            data.extend(current_page_data)

            # 尝试点击下一页
            try:
                next_page_button = driver.find_element(By.CSS_SELECTOR,"li.a-last a")
                if next_page_button:
                    url = next_page_button.get_attribute('href')    # 更新下页的URL
                else:
                    break
            except NoSuchElementException:
                break

    finally:
        driver.quit()


    return data

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.select('div._cDEzb_grid-cell_1uMOS')
    print(f'Number of item: {len(items)}')
    data = []
    for item in items:
        name_div = item.find('div',class_=re.compile(r'_cDEzb_p13n-sc-css-line-clamp-'))
        name = name_div.get_text(strip=True) if name_div else "No Name"

        rating_span = item.find('span',class_='a-icon-alt')
        rating = rating_span.get_text(strip=True) if rating_span else "No rating"

        review_count_span = item.find('span',class_='a-size-small')
        review_count = review_count_span.get_text(strip=True) if review_count_span else "No count"

        price_span = item.find('span',class_='p13n-sc-price')
        price = price_span.get_text(strip=True) if price_span else "No price"

        data.append({'Name': name,
                     'Rating': rating,
                     'Review Count': review_count,
                     'Price': price
                     })

    return data

def save_to_csv(data,filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

