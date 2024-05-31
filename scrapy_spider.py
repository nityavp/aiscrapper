import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls, prompts, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.prompts = prompts
        self.results = []

    def parse(self, response):
        prompt = self.prompts[self.start_urls.index(response.url)]
        matches = response.xpath(f"//*[contains(text(), '{prompt}')]").getall()
        self.results.append({
            'URL': response.url,
            'Prompt': prompt,
            'Matches': matches,
        })

    def closed(self, reason):
        self.crawler.stats.set_value('results', self.results)
