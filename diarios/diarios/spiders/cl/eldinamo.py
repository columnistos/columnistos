# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class EldinamoSpider(scrapy.Spider):
    name = 'eldinamo'
    allowed_domains = ['www.eldinamo.cl/blog']
    start_urls = ['https://www.eldinamo.cl/blog/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url https://www.eldinamo.cl/blog/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//section[@class="listado"]/article')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        #
        loader.add_xpath('author', './/span[@class="autor"]//text()')
        loader.add_xpath('title', './/h1//a//text()')
        loader.add_xpath('url', './/h1//@href')
        return loader.load_item()
