# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class T13Spider(scrapy.Spider):
    name = 't13'
    allowed_domains = ['http://www.t13.cl/opinion/']
    start_urls = ['http://www.t13.cl/opinion/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.t13.cl/opinion/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//article[contains(@class, "a-teaser")]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        loader.add_xpath('title', './/div/h2/a/text()')
        loader.add_xpath('author', 'string(.//div/a/@title)')
        loader.add_xpath('url', 'string(.//div/h2/a/@href)')
        return loader.load_item()
