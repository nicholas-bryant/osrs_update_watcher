from scrapy import Request, Spider, signals
from scrapy.exceptions import DontCloseSpider


class OsrsSpider(Spider):
    name = 'osrs'
    allowed_domains = ['runescape.com']
    start_urls = ['https://oldschool.runescape.com/']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OsrsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def __init__(self):
        self.start_url = 'https://secure.runescape.com/m=news/archive?oldschool=1'
        self.seen = []

    def parse(self, response):
        headlines = response.xpath('//*[@id="newsSection"]/article/div/header/h4/a')
        for headline in headlines:
            url = headline.xpath('./@href').extract_first()
            if url not in self.seen:
                self.seen.append(url)
                print("New Update Found @ " + url)

    def create_start_request(self):
        return Request(self.start_url, self.parse, dont_filter=True)

    def start_requests(self):
        yield self.create_start_request()

    def spider_idle(self):
        self.crawler.engine.crawl(self.create_start_request(), spider=self)
        raise DontCloseSpider("Checking for new updates")
