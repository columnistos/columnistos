# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class Pagina12Spider(scrapy.Spider):
    name = 'pagina12'
    allowed_domains = ['www.pagina12.com.ar']
    start_urls = ['https://www.pagina12.com.ar/']

    def parse(self, response):
        """
        @url https://www.pagina12.com.ar/
        @returns items 0 10
        @returns requests 0 0
        @scrapes author title url
        """
        # cintillo
        selectors = response.css('.opinion-1').xpath(
            './/div[@class="headline-content"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

        # notas en resto del home
        selectors = response.css('.opinion').xpath(
            './/div[@class="headline-content"]')
        for selector in selectors:
            yield self.parse_body(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './div[@class="article-title"]/a/div/text()')
        loader.add_xpath('author', './div[@class="article-author"]/a/text()')
        loader.add_xpath('url', './div[@class="article-title"]/a/@href')
        return loader.load_item()

    def parse_body(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/a[@class="title"]/text()')
        loader.add_xpath('author', './/span[@class="article-author"]/a/text()')
        loader.add_xpath('url', './/a[@class="title"]/@href')
        return loader.load_item()
