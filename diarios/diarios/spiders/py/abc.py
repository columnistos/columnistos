# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class AbcSpider(scrapy.Spider):
    name = 'abc'
    allowed_domains = ['www.abc.com.py']
    start_urls = ['http://www.abc.com.py/edicion-impresa/opinion']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """
        @url http://www.abc.com.py/edicion-impresa/opinion
        @returns items 1 14
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//*[@class="listed"]/ul/li')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        import re
        loader = ItemLoader(DiariosItem(), selector=selector)
        # Busco autor
        autor = selector.xpath('.//h3//text()').extract_first().title().strip()
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        loader.add_value('author', autor)
        # Guardo título
        loader.add_xpath('title', './/h2//a//text()'.strip())
        # Guardo URL
        loader.add_xpath('url', './/h2//@href')
        return loader.load_item()
