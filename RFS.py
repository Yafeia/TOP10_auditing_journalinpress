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
driver.get('https://academic.oup.com/rfs/advance-articles')
time.sleep(5)

# 或者使用显式等待
wait = WebDriverWait(driver, 5)
# wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'issue-item')))

article_list = driver.find_element(By.CLASS_NAME, 'al-article-list-group')
article_items = article_list.find_elements(By.CLASS_NAME, 'al-article-box.al-normal')
data = []
titles_set = set()  # 存储已抓取的标题
for item in article_items:
    title_elements = item.find_elements(By.CLASS_NAME, 'al-title')

    for title_element in title_elements:
        title = title_element.text.strip()

        if title:  # 确保标题不为空
            authors_list = item.find_elements(By.CLASS_NAME, 'al-authors-list')
            authors = [author.text.strip() for author in authors_list]  # 提取所有作者信息
            authors_str = '; '.join(authors)  # 将多个作者信息合并为字符串

            try:
                pub_date_element = item.find_element(By.CLASS_NAME, 'citation-date')
                pub_date = pub_date_element.text.strip()
            except NoSuchElementException:
                pub_date = "unfound"
            
            journal_link_element = item.find_element(By.CLASS_NAME, 'viewArticleLink')  # 定位包含 PDF 链接的元素
            journal_link = journal_link_element.get_attribute("href")

            journal_name = "MS"
            data.append({
                'Title': title,
                'Authors': authors_str if authors_str else None,
                'Publication Date': pub_date,
                'Journallink': journal_link,
                'Journal': journal_name,
            })


# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_RFS_{current_date}.csv'

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
