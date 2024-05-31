import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls  # Store the list of URLs to scrape
        self.results = []  # Initialize an empty list to hold the results

    def parse(self, response):
        url = response.url
        content = response.xpath('//body//text()').getall()  # Extract all text content from the body
        self.results.append({
            'URL': url,
            'Content': " ".join(content).strip(),  # Join the content into a single string
        })

def run_spider(urls):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR"
    })
    spider = MySpider(urls=urls)
    process.crawl(spider)
    process.start()
    return spider.results


