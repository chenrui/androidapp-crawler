# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    category = scrapy.Field()
    apk_from = scrapy.Field()
    apk_name = scrapy.Field()
    apk_url = scrapy.Field()
    apk_version = scrapy.Field()
    apk_path = scrapy.Field()
    task_id = scrapy.Field()
    status = scrapy.Field()
