import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls if urls else []
        self.results = []

    def parse(self, response):
        url = response.url
        content = response.xpath('//body//text()').getall()
        self.results.append({
            'URL': url,
            'Content': " ".join(content).strip(),
        })

def run_spider(urls):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR"
    })
    spider = MySpider(urls=urls)
    process.crawl(spider)
    process.start()  # the script will block here until the crawling is finished
    return spider.results



