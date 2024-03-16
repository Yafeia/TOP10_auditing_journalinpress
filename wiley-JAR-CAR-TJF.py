import os
import re
import requests
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_articles(url, journal_name):
    chrome_options = Options()
    # 添加 Chrome 选项
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'issue-item')))

    article_items = driver.find_elements(By.CLASS_NAME, 'issue-item')

    data = []

    for item in article_items:
        title_elements = item.find_elements(By.CSS_SELECTOR, "h3.issue-item__title.issue-item__title__en")

        for title_element in title_elements:
            title = title_element.text.strip()

            if title:  # 确保标题不为空
                authors_list = item.find_elements(By.CLASS_NAME, 'publication_contrib_author')
                authors = [author.text.strip() for author in authors_list]
                authors_str = '; '.join(authors)

                pub_date_element = item.find_element(By.CLASS_NAME, 'bold')
                pub_date = pub_date_element.text.strip()

                journal_link_element = item.find_element(By.CSS_SELECTOR, 'a[title="ePDF"]')
                journal_link = journal_link_element.get_attribute('href')

                data.append({
                    'Title': title,
                    'Authors': authors_str if authors_str else None,
                    'Publication Date': pub_date,
                    'Journallink': journal_link,
                    'Journal': journal_name
                })

    driver.quit()

    return data

# 传入多个不同的 URL 进行爬取
urls = ['https://onlinelibrary.wiley.com/journal/1475679X', # Journal of Accounting Research
        'https://onlinelibrary.wiley.com/journal/19113846', # Contemporary Accounting Research (CAR)
        'https://onlinelibrary.wiley.com/journal/15406261',  # The Journal of Finance
        ]
journal_names = ['Journal of Accounting Research', 
                 'Contemporary Accounting Research (CAR)', 
                 'The Journal of Finance',
                 ]
all_data = []

for i, url in enumerate(urls):
    data = scrape_articles(url, journal_names[i])
    all_data.extend(data)

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_JAR_CAR_TJF{current_date}.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Authors', 'Publication Date', 'Journallink', 'Journal']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f'Data has been successfully written to {csv_file}')

# # 创建文件夹用于存储下载的 PDF
# download_folder = rf'F:\论文\230-华中科技大学\文献\wiley_JAR_CAR_TJF_{current_date}'
# os.makedirs(download_folder, exist_ok=True)

# for article in all_data:
#     title = article['Title']
#     journal = article['Journal']
#     journal_link = article['Journallink']
#     file_path = os.path.join(download_folder, f"{title}.pdf")  # 构建保存文件的完整路径

#     # 假设 journal_link 是一个包含 PDF 阅读器和下载按钮的页面链接
#     response = requests.get(journal_link)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # 找到包含 PDF 下载链接的元素，通常可以通过查找包含特定文本的<a>标签来实现
#     download_elements = soup.find_all('a', href=True)

#     for element in download_elements:
#         if "/doi/pdfdirect/" in element['href']:
#             pdf_link = "https://onlinelibrary.wiley.com" + element['href']  # 构建完整的下载链接

#             # 下载 PDF
#             response = requests.get(pdf_link)
#             if response.status_code == 200:
#                 with open(file_path, 'wb') as file:  # 将文件保存为特定的文件名
#                     file.write(response.content)
#                 print(f'PDF file "{title}" downloaded successfully')
#             else:
#                 print(f'Failed to download PDF file "{title}"')
