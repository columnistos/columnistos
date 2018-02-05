# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class LaterceraSpider(scrapy.Spider):
    name = 'latercera'
    allowed_domains = ['latercera.com']
    start_urls = ['http://www.latercera.com/etiqueta/voces/']

    def parse(self, response):
        """
        @url http://www.latercera.com/etiqueta/voces/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//article[@class="border-bottom-1 archive-article"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('author', './/p//small[2]//a//text()')
        loader.add_xpath('title', './/h4//text()')
        loader.add_xpath('url', './/h4//@href')
        print(loader.__dict__.keys())
        print(loader._local_values)
        return loader.load_item()
