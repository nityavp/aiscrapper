import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

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
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(MySpider, urls=urls)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    return runner.spider.results






