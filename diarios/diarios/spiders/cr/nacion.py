# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem

import logging


class NacionSpider(scrapy.Spider):
    name = 'nacion'
    allowed_domains = ['www.nacion.com']
    start_urls = ['http://www.nacion.com/opinion/columnistas/']

    def parse(self, response):
        """
        @url http://www.nacion.com/opinion/columnistas/
        @returns items 1 15
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="generic-results-list-item"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        import re

        loader = ItemLoader(item=DiariosItem(), selector=selector)

        titulo = selector.xpath('./article//figure/a/h4/text()').extract_first()
        titulo = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', titulo)
        loader.add_value('title', titulo)

        autor = selector.xpath('./article//figure//div[@class="byline"]/span[@class="author"]//text()').extract_first()
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        loader.add_value('author', autor)

        loader.add_xpath('url', './article//figure/a/@href')

        return loader.load_item()
