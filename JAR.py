import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
# chrome_options.add_argument('--headless')  # 无头模式
# chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误

# 使用Selenium打开网页
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://onlinelibrary.wiley.com/journal/1475679X')
time.sleep(5)

# 或者使用显式等待
wait = WebDriverWait(driver, 5)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'issue-item')))

article_items = driver.find_elements(By.CLASS_NAME, 'issue-item')

data = []
titles_set = set()  # 存储已抓取的标题

for item in article_items:
    title_elements = item.find_elements(By.CSS_SELECTOR, "h3.issue-item__title.issue-item__title__en")

    for title_element in title_elements:
        title = title_element.text.strip()

        if title not in titles_set:  # 判断标题是否已经存在，如果不存在则进行处理
            titles_set.add(title)

            # 处理作者
            authors_list = item.find_elements(By.CLASS_NAME, 'publication_contrib_author')
            authors = [author.text.strip() for author in authors_list]
            authors_str = '; '.join(authors)

            # 处理出版日期
            pub_date_element = item.find_element(By.CLASS_NAME, 'bold')
            pub_date = pub_date_element.text.strip()

            # 处理期刊链接 
            journal_link_element = item.find_element(By.CSS_SELECTOR, 'a[title="ePDF"]')
            journal_link = journal_link_element.get_attribute('href')

            journal_name = 'Journal of Accounting Research'

            data.append({
                'Title': title,
                'Authors': authors_str,
                'Publication Date': pub_date,
                'Journallink': journal_link,
                'Journal': journal_name
            })


# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_JAR_{current_date}.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Title',
                 'Authors',
                 'Publication Date',
                 'Journallink',
                 'Journal',
                 ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f'Data has been successfully written to {csv_file}')

# 关闭浏览器
driver.quit()
