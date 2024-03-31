import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver.common.by import By
from datetime import datetime

# 发送网络请求获取页面内容
url = "https://link.springer.com/journal/11142"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)
response.raise_for_status()

# 解析页面内容
soup = BeautifulSoup(response.text, "html.parser")

# 提取所需信息
article_items = soup.find_all("div", class_="c-card-open__main")

data = []

for item in article_items:
    title = item.find("h3", class_="c-card-open__heading").text.strip()
    authors_list = item.find_all("li", class_="c-author-list__item")
    authors = []
    for author_item in authors_list:
        author = author_item.text.strip()
        authors.append(author)

    # 将作者列表转换为以逗号分隔的字符串
    authors_str = ', '.join(authors)
    pub_datelist = item.find_all("span", class_="c-meta__item")
    pub_dates = []
    for pub_date_item in pub_datelist:
        pub_date = pub_date_item.text.strip()
        pub_dates.append(pub_date)
    # pub_date = item.find("span", class_="c-meta__item")
    # journal_link_element = item.find_element(By.XPATH, ".//a[@title='PDF']")  # 定位包含 PDF 链接的元素
    # journal_link = journal_link_element.get_attribute("href")
    journal_link ="no pdf link found"
    journal_name = "Review of Accounting Studies"

    data.append({'Title': title,
                 'Authors': authors,
                 'Publication Date': pub_date,
                 'Journallink': journal_link,
                 'Journal': journal_name,
                 })

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_RAS_{current_date}.csv'

# 写入CSV文件
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames =  ['Title',
                 'Authors',
                 'Publication Date',
                 'Journallink',
                 'Journal',
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print(f"Data has been successfully written to {csv_file}")
