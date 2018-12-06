# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class DelfinoSpider(scrapy.Spider):
    name = 'delfino'
    allowed_domains = ['delfino.cr']
    start_urls = [
        'https://delfino.cr/columnas/'
    ]

    def parse(self, response):
        """
        @url http://delfino.cr/opinion/
        @returns items 1 18
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="author-item"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './a[not(@class)]/h3/text()')
        loader.add_xpath('author', './a[@class="author-name"]/text()')
        loader.add_xpath('url', './a[not(@class)]/@href')

        return loader.load_item()
