import scrapy
from scrapy.crawler import CrawlerProcess
import csv
from datetime import datetime

class JournalSpider(scrapy.Spider):
    name = "journal_spider"

    # 定义不同期刊的网页链接
    start_urls = [
        'https://publications.aaahq.org/accounting-review/publish-ahead-of-print', #accounting-review
        'https://link.springer.com/journal/11142', #Review of Accounting Studies
        'https://onlinelibrary.wiley.com/journal/1475679X', #Journal of Accounting Research
        'https://onlinelibrary.wiley.com/journal/19113846', #Contemporary Accounting Research (CAR)
        'https://onlinelibrary.wiley.com/journal/15406261', #The Journal of Finance
        'https://www.sciencedirect.com/journal/journal-of-accounting-and-economics/articles-in-press', #Journal of Accounting and Economics
        'https://www.sciencedirect.com/journal/accounting-organizations-and-society/articles-in-press', #Accounting, Organizations and Society
        'https://www.sciencedirect.com/journal/journal-of-financial-economics', #The Journal of Financial Economics (JFE)
        'https://pubsonline.informs.org/toc/mnsc/0/0', #Management science
        'https://academic.oup.com/rfs/advance-articles', #Review of Financial Studies
    ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # 根据不同期刊的结构编写解析逻辑
        if 'https://publications.aaahq.org/accounting-review/publish-ahead-of-print' in response.url:
            article_items = response.css('.article')
            for item in article_items:
                title = item.css('h3.c-card-open__heading::text').get()
                authors_list = item.css('li.c-author-list__item')
                authors = [author.css('::text').get().strip() for author in authors_list]
                authors_str = ', '.join(authors)
                pub_dates = item.css('span.c-meta__item::text').getall()
                journal_name = 'Journal 1'

                yield {
                    'title': title,
                    'authors': authors_str,
                    'Publication Date': pub_dates[0] if pub_dates else '',
                    'Journal': journal_name
                }
        
        elif 'https://link.springer.com/journal/11142' in response.url:
            article_items = response.css('.article')
            for item in article_items:
                title = item.css('h5.al-title::text').get()
                authors_list = item.css('span.wi-fullname.brand-fg')
                authors = [author.css('::text').get().strip() for author in authors_list]
                authors_str = ';'.join(authors)
                pub_date = item.css('span.sri-date.al-pub-date::text').get()
                journal_elem = item.css('div.ww-citation-primary')
                journal_name = journal_elem.css('em::text').get() if journal_elem.css('em') else 'N/A'

                yield {
                    'Title': title,
                    'Authors': authors_str,
                    'Publication Date': pub_date,
                    'Journal': journal_name
                }


current_date = datetime.now().strftime("%Y-%m-%d")
csv_file = rf'F:\论文\230-华中科技大学\文献\文献_{current_date}.csv'

# 创建一个 CSV 文件用于存储爬取的数据
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Authors', 'Publication Date', 'Journal'])
    writer.writeheader()

    process = CrawlerProcess(settings={
        'FEEDS': {
            csv_file: {'format': 'csv'},
        }
    })
    process.crawl(JournalSpider)
    process.start()

print(f"Data has been successfully written to {csv_file}")