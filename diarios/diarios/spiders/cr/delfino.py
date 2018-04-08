# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class DelfinoSpider(scrapy.Spider):
    name = 'delfino'
    allowed_domains = ['nacion.com']
    start_urls = [
        'http://delfino.cr/opinion/'
    ]

    def parse(self, response):
        """
        @url http://delfino.cr/opinion/
        @returns items 1 12
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//article/div/div[@class="column"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        import re

        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/h3[@class="news-card-title"]/a/text()')

        #capitalizar el titulo y quitar los 4 primeros caracteres que es el "Por "
        autor = response.xpath('.//h5[@class="author"]/text()').extract_first().title()[4:]
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        loader.add_value('author', autor)
        
        loader.add_xpath('url', './/h3[@class="news-card-title"]/a/@href')
        return loader.load_item()
