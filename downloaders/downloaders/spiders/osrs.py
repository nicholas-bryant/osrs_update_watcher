from scrapy import Request, Spider


class OsrsSpider(Spider):
    name = 'osrs'
    allowed_domains = ['runescape.com']
    start_urls = ['https://oldschool.runescape.com/']

    def parse(self, response):
        print(response.body)

    def start_requests(self):
        yield Request(
            'https://oldschool.runescape.com/',
            self.parse
        )
