
import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re


def scrape_articles(url, journal_name):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)

    article_list = driver.find_element(By.CLASS_NAME, 'js-article-list.article-list-items')
    article_items = article_list.find_elements(By.TAG_NAME, 'li')
    data = []

    for item in article_items:
        title_elements = item.find_elements(By.CLASS_NAME, 'js-article-title')

        for title_element in title_elements:
            title = title_element.text.strip()
            # 替换特殊字符
            title_for_filename = re.sub(r'[\\/*?:"<>|]', '+', title)

            if title:
                authors_list = item.find_elements(By.CLASS_NAME, 'text-s.u-clr-grey8.js-article__item__authors')
                authors = [author.text.strip() for author in authors_list]
                authors_str = '; '.join(authors)

                try:
                    pub_date_element = item.find_element(By.CLASS_NAME, 'u-clr-grey8.u-text-italic.text-s.js-article-item-aip-date')
                    pub_date = pub_date_element.text.strip()
                except NoSuchElementException:
                    pub_date = "unfound"
                journal_link_element = item.find_element(By.XPATH,'//*[@id="article-list"]/form/div/div[2]/ol/li[1]/dl/dd[3]/a')  # 定位包含 PDF 链接的元素
                journal_link = journal_link_element.get_attribute("href")
               
                data.append({
                    'Title': title,
                    'Authors': authors_str if authors_str else None,
                    'Publication Date': pub_date,
                    'Journallink': journal_link,
                    'Journal': journal_name,
                })

    driver.quit()
    return data


urls = [
    'https://www.sciencedirect.com/journal/accounting-organizations-and-society/articles-in-press',
    'https://www.sciencedirect.com/journal/journal-of-accounting-and-economics/articles-in-press'
]

journal_names = [
    'AOS-Accounting Organizations and Society',
    'JAE-Journal of Accounting and Economics'
]

all_data = []

# 爬取文章数据
for url, journal_name in zip(urls, journal_names):
    data = scrape_articles(url, journal_name)
    all_data.extend(data)

# 写入CSV文件
current_date = datetime.now().strftime('%Y-%m-%d')
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_AOS_JAE_{current_date}.csv'

with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Title', 
                 'Authors', 
                 'Publication Date',
                 'Journallink',
                 'Journal',
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:  # 如果文件为空，则写入表头
        writer.writeheader()
    writer.writerows(all_data)

print(f'Data has been successfully written to {csv_file}')

