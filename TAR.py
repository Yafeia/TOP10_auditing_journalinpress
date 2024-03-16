import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 发送网络请求获取页面内容
url = "https://publications.aaahq.org/accounting-review/publish-ahead-of-print"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 提取数据...


# 提取所有标题、作者、出版日期和期刊名称
article_items = soup.find_all("div", class_="al-article-items")

data = []

for item in article_items:
    title = item.find("h5", class_="al-title").text.strip()
    authors = item.find_all("span", class_="wi-fullname brand-fg")
    author_names = ";".join([author.text.strip() for author in authors])
    pub_date = item.find("span", class_="sri-date al-pub-date").text.strip()
    journal_elem = item.find("div", class_="ww-citation-primary")
    journal_name = journal_elem.find("em").text if journal_elem.find("em") else "N/A"
    data.append({'title': title, 'authors': author_names, 'Publication Date': pub_date, 'Journal': journal_name})

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_TAR_{current_date}.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'authors', 'Publication Date', 'Journal']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print(f"Data has been successfully written to {csv_file}")
