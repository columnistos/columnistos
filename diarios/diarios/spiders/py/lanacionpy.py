# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from diarios.items import DiariosItem

logging.basicConfig(level=logging.DEBUG)

class LanacionpySpider(scrapy.Spider):
    name = 'lanacionpy'
    allowed_domains = ['www.lanacion.com.py']
    start_urls = ['http://www.lanacion.com.py/category/columnistas']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.lanacion.com.py/category/columnistas
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//*[@id="west"]/div/div[2]/div[1]/div[2]/div/article')
        for selector in selectors:
            link = response.urljoin(selector.xpath('.//@href').extract_first())
            if link is not None:
                yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        import re
        selector = response.xpath('//*[@id="article-content"]')
        loader = ItemLoader(DiariosItem(), selector=selector)
        #Extraigo autor y convierto en mayus y borro espacios
        autor = response.xpath('.//b//text()').extract()
        # Saco símbolos raros
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        # Trae "Por" al principio así que lo saco
        for x in autor:
            # Lo paso todo primera mayus y saco espacios
            x = x.title().strip()
            # Recorro y saco "Por"
            if x[:4] == "Por ":
                autor = autor[4:]
        # Guardo autor
        loader.add_value('author', autor)
        # Guardo título
        loader.add_value('title', response.xpath('//*[@class="headline huge normal-style "]/a/text()').extract_first().strip())
        # Guardo URL
        loader.add_value('url', response.request.url)
        return loader.load_item()
