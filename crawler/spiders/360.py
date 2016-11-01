import scrapy
from scrapy.spiders import Spider
from crawler.items import CrawlerItem
from crawler.loader import APKItemLoader


class Spider360(Spider):
    name = '360'
    host = 'http://zhushou.360.cn'

    def start_requests(self):
        start_urls = [self.host + '/list/index/cid/1',
                      self.host + '/list/index/cid/2']
        for url in start_urls:
            yield scrapy.Request(url, self.parse_category)

    def parse_category(self, response):
        for position in response.xpath('//ul[@class="select"]/li'):
            cates = position.xpath('a[starts-with(@href, "/list/index/cid")]/text()').extract()
            urls = position.xpath('a[starts-with(@href, "/list/index/cid")]/@href').extract()
            cates = cates[1:]
            urls = urls[1:]
            for cate, url in zip(cates, urls):
                base_url = self.host + url + '?page='
                for page in xrange(1, 51):
                    url = base_url + str(page)
                    yield scrapy.Request(url, self.parse_apk, meta={'cate': cate})

    def parse_apk(self, response):
        for position in response.xpath('//ul[@id="iconList"]/li'):
            l = APKItemLoader(item=CrawlerItem(), selector=position)
            l.add_value('category', response.meta.get('cate', ''))
            l.add_value('apk_from', '360')
            l.add_xpath('apk_name', 'h3/a/text()')
            l.add_xpath('apk_url', 'a[starts-with(@href, "zhushou360:")]/@href', re=r'.*&url=(.*)')
            yield l.load_item()


