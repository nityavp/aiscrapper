import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

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
    configure_logging()
    runner = CrawlerRunner()
    
    @defer.inlineCallbacks
    def crawl():
        spider = MySpider(urls=urls)
        yield runner.crawl(spider)
        reactor.stop()
        return spider.results

    crawl()
    reactor.run()  # the script will block here until the crawling is finished
    return spider.results







