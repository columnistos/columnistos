# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class TheclinicSpider(scrapy.Spider):
    name = 'theclinic'
    allowed_domains = ['www.theclinic.cl/columnas-y-entrevistas/']
    start_urls = ['http://www.theclinic.cl/columnas-y-entrevistas/']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.theclinic.cl/columnas-y-entrevistas/
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="scope entramado"]//div[@class="item"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        #
        author = selector.xpath('.//span[@class="author"]').extract()[0][5:]
        loader.add_value('author', author)
        loader.add_xpath('title', './/div[@class="nota"]//a//text()')
        loader.add_xpath('url', './/div[@class="nota"]//@href')
        return loader.load_item()
