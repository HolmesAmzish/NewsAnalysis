"""
file: news_getter.py
version: 1.0 2024-12-29
since: 2024-12-29
author: Cacc
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import datetime
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import shutil

DRIVER_PATH = "./chromedriver"


def get_driver():
    if not os.path.exists(DRIVER_PATH):
        driver_path = ChromeDriverManager().install()
        shutil.copy(driver_path, DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(service=Service(DRIVER_PATH), options=options)

driver = get_driver()


def get_links():
    # Parse js code and get page content by selenium
    # Set the root page for sina news
    root_url = "https://news.sina.com.cn/roll/"
    driver.get(root_url)
    driver.implicitly_wait(5)
    content = driver.page_source

    # Get news list by regex
    pattern = r"https://finance\.sina\.com\.cn/[a-zA-Z0-9/_-]+/doc-[a-zA-Z0-9]+\.shtml"
    news_list = re.findall(pattern, content)

    return news_list


def save_news_html(news_list):
    """
    Save all content from news list link by html form
    :param news_list: List of news urls
    :return None
    """
    for news_link in news_list:
        driver.get(news_link)
        driver.implicitly_wait(5)
        content = driver.page_source

        file_name = re.search(r'doc-([a-zA-Z0-9]+)\.shtml', news_link).group(1)
        with open(f"saved_news/{file_name}.html", "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Saved: {file_name}.html")


def get_content_from_file(filepath):
    """
    Get raw content from html file
    :param filepath: path of saved file
    :return a raw html content
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        return content


def get_news_content_from_url(url):
    """
    Get news content from html content
    Record url, title, time and article
    :param url
    :return: news content_dict
    """
    news_dict = {'url': url}

    driver.get(url)
    driver.implicitly_wait(5)
    content = driver.page_source

    soup = BeautifulSoup(content, 'lxml')
    news_title = soup.select('h1.main-title')[0].text.strip()
    news_dict['title'] = news_title

    news_time_temp = datetime.datetime.strptime(
        soup.select('span.date')[0].text.strip(),
        '%Y年%m月%d日 %H:%M'
    )

    news_time = (news_time_temp

                 .strftime('%Y-%m-%d %H:%M:%S'))
    news_dict['time'] = news_time

    news_article = soup.select('div#artibody p')

    news_article_text = ''
    for paragraph in news_article:
        news_article_text += paragraph.text.strip()
    news_dict['article_text'] = news_article_text

    return news_dict
