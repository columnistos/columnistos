# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class CooperativaSpider(scrapy.Spider):
    name = 'cooperativa'
    allowed_domains = ['www.cooperativa.cl/opinion/']
    start_urls = ['http://www.cooperativa.cl/opinion/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.cooperativa.cl/opinion/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//section[@id="modulo-varios-2"]//article')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        print('ghola')
        loader = ItemLoader(DiariosItem(), selector=selector)
        #
        author = selector.xpath('.//div[@class="contenedor-nombre-perfil"]//text()').extract()[0][4:]
        print(author)
        loader.add_value('author', author)
        loader.add_xpath('title', './/h3//text()')
        loader.add_xpath('url', './/@href[1]')
        return loader.load_item()
