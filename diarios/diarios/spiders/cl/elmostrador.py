# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class ElmostradorSpider(scrapy.Spider):
    name = 'elmostrador'
    allowed_domains = ['www.elmostrador.cl/noticias/opinion/columnas']
    start_urls = ['http://www.elmostrador.cl/noticias/opinion/columnas/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.elmostrador.cl/noticias/opinion/columnas/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//section[@class="col-xs-12 col-sm-12 col-md-12 lo-ultimo"]//article')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        #
        author = selector.xpath('.//p//text()').extract()[0][4:]
        loader.add_value('author', author)
        loader.add_xpath('title', './/h4//text()')
        loader.add_xpath('url', './/h4//@href')
        return loader.load_item()
