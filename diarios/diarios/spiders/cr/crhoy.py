# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem

import logging


class CRHoySpider(scrapy.Spider):
    name = 'crhoy'
    allowed_domains = ['www.crhoy.com']
    start_urls = ['https://www.crhoy.com/site/generators/category.php?cat=7809&cant=20&text=300&current=1&date=1&portada=0&author=1']

    def parse(self, response):
        """
        @url https://www.crhoy.com/site/generators/category.php?cat=7809&cant=20&text=300&current=1&date=1&portada=0&author=1
        @returns items 1 20
        @returns requests 0 0
        @scrapes author title url
        """

        jsonresponse = json.loads(response.body_as_unicode())['noticiasCategoria']
        for article in jsonresponse:
            yield self.parse_article(article)

    def parse_article(self, article):

        loader = ItemLoader(item=DiariosItem())
        loader.add_value('title', article['title'])
        loader.add_value('author', article['author'][0])
        loader.add_value('url', article['url'])

        return loader.load_item()
