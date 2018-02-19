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
        selectors = response.xpath('//*[@class="object-opinion-2016"]/div[2]/div/div')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        #
        loader.add_xpath('author', './/span//a//text()')
        loader.add_xpath('title', './/h3//a//text()')
        loader.add_xpath('url', './/h3//@href')
        return loader.load_item()
