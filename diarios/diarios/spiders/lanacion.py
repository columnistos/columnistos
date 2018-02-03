# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class LanacionSpider(scrapy.Spider):
    name = 'lanacion'
    allowed_domains = ['www.lanacion.com.ar']
    start_urls = ['http://www.lanacion.com.ar/']

    def parse(self, response):
        """
        @url http://www.lanacion.com.ar/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//*[@id="autores"]/article')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/h2//text()')
        loader.add_xpath('author', './/a[@class="nombre"]/text()')
        loader.add_xpath('url', './/h2//@href')
        return loader.load_item()
