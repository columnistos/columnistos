# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class PerfilSpider(scrapy.Spider):
    name = 'perfil'
    allowed_domains = ['www.perfil.com']
    start_urls = ['http://www.perfil.com/']

    def parse(self, response):
        """
        @url http://www.perfil.com/
        @returns items 1 30
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//*[@id="myCarouselOpinion"]//article')
        if len(selectors) > 0:
            for selector in selectors:
                yield self.parse_article(selector, response)
        else:
            selectors = response.xpath('//section[@class="opinion"]//article')
            for selector in selectors:
                yield self.parse_sunday(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './h5/a/text()')
        loader.add_xpath('author', './p/a/text()')
        loader.add_xpath('url', './h5/a/@href')
        return loader.load_item()

    def parse_sunday(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './/p[@class="lead"]/a/text()')
        loader.add_xpath('author', './/p[@class="by-line"]/a/text()')
        loader.add_xpath('url', './/p[@class="lead"]/a/@href')
        return loader.load_item()
