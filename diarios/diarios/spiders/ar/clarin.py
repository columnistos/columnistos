# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from diarios.items import DiariosItem


class ClarinSpider(scrapy.Spider):
    name = 'clarin'
    allowed_domains = ['www.clarin.com']
    start_urls = ['https://www.clarin.com/']

    def parse(self, response):
        """
        gets main page and links to jsons

        @url https://www.clarin.com/
        @returns requests 1 15
        """
        # main page
        # articulos de opinión en cuerpo
        selectors = Selector(text=response.text).xpath(
            '//div[@class="data-txt"]//p[contains(.,"Opinión")]')
        for selector in selectors:
            yield self.parse_article_body(selector, response)

        selectors = response.xpath(
            '//*[@id="columnas"]//div[@class="mt"]')
        for selector in selectors:
            yield self.parse_article_grouped(selector, response)


        # links to jsons
        on_demand = response.xpath(
            '//*[@class="on-demand"]//@data-src')
        for link in on_demand:
            next_page = response.urljoin(link.extract())
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_json)

    def parse_json(self, response):
        json_data = json.loads(response.text[1:-1])
        sel = Selector(text=json_data['data'])

        # opinión agrupado
        selectors = sel.xpath(
            '//*[@id="columnas"]//div[@class="mt"]')
        for selector in selectors:
            yield self.parse_article_grouped(selector, response)

        # articulos de opinión en cuerpo
        selectors = sel.xpath(
            '//div[@class="data-txt"]//p[contains(.,"Opinión")]')
        for selector in selectors:
            yield self.parse_article_body(selector, response)

    def parse_article_grouped(self, selector, response):
        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title', './h2/text()')
        loader.add_xpath('author', './span[@class="author-name"]/text()')
        loader.add_xpath('url', './ancestor::div/a/@href')
        return loader.load_item()

    def parse_article_body(self, selector, response):
        # check if article has no author
        if selector.xpath('./ancestor::div[@class="data-txt"]/p') == []:
            return

        loader = ItemLoader(DiariosItem(), selector=selector)

        loader.add_xpath('title',
                         './ancestor::article/div[@class="mt"]/a/h2/text()')
        loader.add_xpath('url',
                         './ancestor::article/div[@class="mt"]/a/@href')
        loader.add_xpath('author',
                         './ancestor::div[@class="data-txt"]/p/text()')
        return loader.load_item()
