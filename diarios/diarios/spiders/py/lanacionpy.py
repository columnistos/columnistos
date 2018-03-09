# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


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
        #capitalizar el titulo y quitar los 4 primeros caracteres que es el "Por "
        autor = response.xpath('//strong//text()').extract_first().title()[4:]
        #autor = re.sub('[\.(*)]', '', autor)
        autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor)
        loader.add_value('author', autor)
        loader.add_value('title', response.xpath('//*[@class="headline huge normal-style "]/a/text()').extract_first())
        loader.add_value('url', response.request.url)
        return loader.load_item()
