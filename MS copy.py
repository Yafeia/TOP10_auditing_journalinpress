import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',

    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',

    'Accept-Encoding': 'gzip, deflate, br',

    'Connection': 'keep-alive',

    'Upgrade-Insecure-Requests': '1'}

# 设置 Chrome 选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

url = "https://pubsonline.informs.org/journal/mnsc"

# 使用 Selenium 打开网页
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(10)
# 提取所需信息
elements = driver.find_elements(By.CLASS_NAME, 'issue-item__title')

data = []

for element in elements:
    # 获取链接地址
    href = element.find_element(By.TAG_NAME, 'a').get_attribute('href')

    # 打开新页面
    driver.execute_script(f"window.open('{href}','_blank')")
    driver.switch_to.window(driver.window_handles[1])
    driver.set_window_size(1000, 800)
    time.sleep(30)
    # 提取所需信息
    title = driver.find_element(By.CLASS_NAME, 'citation__title').text.strip()
    authors = '; '.join([author.text.strip() for author in driver.find_elements(By.CLASS_NAME, 'entryAuthor')]) 
    abstract = driver.find_element(By.CLASS_NAME, 'abstractSection').text.strip()
    pub_date = driver.find_element(By.CLASS_NAME, 'epub-section__date').text.strip()

    # 添加数据到列表
    data.append({
        'Title': title,
        'Authors': authors,
        'Abstract': abstract,
        'Publication Date': pub_date,
        # 其他字段...
    })

    # 关闭新页面
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# 写入 CSV 文件
current_date = datetime.now().strftime("%Y-%m-%d")
csv_file = f'F:\\论文\\230-华中科技大学\\文献\\文献_RAS_{current_date}.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Title', 'Authors', 'Abstract', 'Publication Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been successfully written to {csv_file}")

# 退出浏览器
driver.quit()
