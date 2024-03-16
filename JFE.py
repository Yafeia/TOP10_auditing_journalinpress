import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



chrome_options = Options()
# chrome_options.add_argument('--headless')  # 无头模式
# chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误

# 使用Selenium打开网页
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.sciencedirect.com/journal/journal-of-financial-economics/vol/articles-in-press')
time.sleep(5)

# 或者使用显式等待
wait = WebDriverWait(driver, 5)
# wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'issue-item')))

article_list = driver.find_element(By.CLASS_NAME, 'js-article-list.article-list-items')
article_items = article_list.find_elements(By.TAG_NAME, 'li')
data = []
titles_set = set()  # 存储已抓取的标题

for item in article_items:
    title_elements = item.find_elements(By.CLASS_NAME, 'js-article-title')

    for title_element in title_elements:
        title = title_element.text.strip()

        if title:  # 确保标题不为空
            authors_list = item.find_elements(By.CLASS_NAME, 'text-s u-clr-grey8 js-article__item__authors')
            authors = [author.text.strip() for author in authors_list]
            authors_str = '; '.join(authors)

            try:
                pub_date_element = item.find_element(By.CLASS_NAME, 'u-clr-grey8.u-text-italic.text-s.js-article-item-aip-date')
                pub_date = pub_date_element.text.strip()
            except NoSuchElementException:
                pub_date = "unfound"
            journal_link_element = item.find_element(By.CLASS_NAME, 'anchor.pdf-download.u-margin-l-right.text-s.anchor-default.anchor-icon-left')
            journal_link = journal_link_element.get_attribute('href')
            journal_name="SC"
            data.append({
                'Title': title,
                'Authors': authors_str if authors_str else None,
                'Publication Date': pub_date,
                'Journallink': journal_link,
                'Journal': journal_name ,
            })

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_{current_date}.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Authors', 'Publication Date', 'Journallink', 'Journal']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f'Data has been successfully written to {csv_file}')

# 关闭浏览器
driver.quit()
