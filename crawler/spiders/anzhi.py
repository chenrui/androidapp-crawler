import re
import scrapy
from scrapy.spiders import Spider
from crawler.items import CrawlerItem
from crawler.loader import APKItemLoader


class SpiderAnZhi(Spider):
    name = 'anzhi'
    host = 'http://www.anzhi.com'

    def start_requests(self):
        start_urls = [self.host + '/applist.html',
                      ]
        for url in start_urls:
            yield scrapy.Request(url, self.parse_category)

    def parse_category(self, response):
        compile = re.compile(r'widgetsort_(.*)_1_3.html')
        for pos in response.xpath('//div[@class="content_left"]/div[@class="item_wrap"]/div[@class="border_three"]'):
            scripts = pos.xpath('script/text()').extract()
            for js in scripts:
                js = js.strip()
                index = compile.search(js).group(1)
                url = self.host + '/sort_%s_1_hot.html' % index
                yield scrapy.Request(url, self.parse_apk)

    def parse_apk(self, response):
        compile = re.compile(r'opendown\((.*)\)')
        cate = response.xpath('//div[@class="title"]/h2/text()').extract_first()
        next = response.xpath('//div[@class="pagebars"]/a[@class="next"]/@href').extract_first()
        for position in response.xpath('//div[@class="app_list border_three"]/ul/li'):
            dl = position.xpath('div[@class="app_down"]/a/@onclick').extract_first()
            dl = self.host + '/dl_app.php?s=%s&n=5' % compile.search(dl).group(1)
            l = APKItemLoader(item=CrawlerItem(), selector=position)
            l.add_value('category', cate)
            l.add_value('apk_from', 'anzhi')
            l.add_value('apk_url', [dl])
            l.add_xpath('apk_name', 'div[@class="app_info"]/span/a/text()')
            yield l.load_item()

        if next:
            url = self.host + next
            yield scrapy.Request(url, self.parse_apk)



