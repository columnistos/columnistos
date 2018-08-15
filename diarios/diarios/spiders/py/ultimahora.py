# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class UltimahoraSpider(scrapy.Spider):
    name = 'ultimahora'
    allowed_domains = ['www.ultimahora.com']
    start_urls = ['http://www.ultimahora.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.ultimahora.com
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="persons"]/div/div')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        import re
        loader = ItemLoader(DiariosItem(), selector=selector)
        #Extraigo autor y convierto en mayus y borro espacios
        autor = selector.xpath('//div[@class="person-name"]//text()').extract_first().title().strip()
        # Saco símbolos raros
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        # Trae "Por" al principio así que lo saco
        if autor[:4] == "Por ":
            autor = autor[4:].strip()
        # Guardo autor
        loader.add_value('author', autor)
        # Guardo título
        loader.add_xpath('title', './/h3//text()'.strip())
        # Guardo URL
        loader.add_xpath('url', './/h3//@href')
        return loader.load_item()
