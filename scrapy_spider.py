import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        if urls:
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
    configure_logging()
    runner = CrawlerRunner()
    
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(MySpider, urls=urls)
        reactor.stop()
    
    crawl()
    reactor.run()  # the script will block here until the crawling is finished
    return MySpider(urls=urls).results








