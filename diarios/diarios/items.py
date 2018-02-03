# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiariosItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    added = scrapy.Field(serializer=str)
    last_seen = scrapy.Field(serializer=str)
