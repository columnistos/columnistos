# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class LaRepublicaSpider(scrapy.Spider):
    name = 'larepublica'
    allowed_domains = ['larepublica.net']
    start_urls = [
        'https://www.larepublica.net/seccion/opinion/'
    ]

    def parse(self, response):
        """
        @url https://www.larepublica.net/seccion/opinion
        @returns items 1 4
        @returns requests 0 0
        @scrapes author title url
        """
        selectors = response.xpath('//div[@class="content-block"]')
        for selector in selectors:
            yield self.parse_article(selector, response)

    def parse_article(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)
        loader.add_xpath('title', './a/h2/text()')
        loader.add_xpath('author', './div/a[position()=2]/text()')
        loader.add_xpath('url', './a/@href')
        return loader.load_item()
