# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class NacionSpider(scrapy.Spider):
    name = 'nacion'
    allowed_domains = ['www.nacion.com']
    start_urls = [
        'http://www.nacion.com/opinion/columnistas/'
    ]

    def parse(self, response):
        """
        @url http://www.nacion.com/
        @returns items 1 15
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="generic-results-list-item"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/article//figure/a/h4/text()')
        loader.add_xpath(
            'author',
            './/article//figure/div/span[@class="autor"]/a/text()'
        )
        loader.add_xpath('url', './/article//figure/a[@href]')
        return loader.load_item()
