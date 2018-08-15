# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class DelfinoSpider(scrapy.Spider):
    name = 'delfino'
    allowed_domains = ['delfino.cr']
    start_urls = [
        'http://delfino.cr/opinion/'
    ]

    def parse(self, response):
        """
        @url http://delfino.cr/opinion/
        @returns items 1 6
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="card-body"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/h3[@class="card-title"]/text()')

        # Quitar los 4 primeros caracteres "Por "
        autor = selector.xpath('./h5[@class="card-author"]/text()').extract_first().title()[4:]
        loader.add_value('author', autor)
        
        loader.add_xpath('url', './a/@href')
        return loader.load_item()
