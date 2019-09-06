# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy.loader import ItemLoader

from diarios.items import DiariosItem


class AbcSpider(scrapy.Spider):
    name = 'abc'
    limit_articles = '50'
    allowed_domains = ['www.abc.com.py']
    start_urls = ['https://www.abc.com.py/pf/api/v3/content/' +
                  'fetch/sections-api?query={"arc-site":"abccolor"' +
                  ',"id":"/edicion-impresa/opinion","limit":"' +
                  limit_articles + '","offset":0,' +
                  '"uri":"/edicion-impresa/opinion/"}']
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
        items = json.loads(response.text)
        for item in items['content_elements']:
            yield self.parse_article(item)

    def parse_article(self, item):
        loader = ItemLoader(DiariosItem())
        for cred in item['credits']['by']:
            if cred['type'] == 'author':
                autor = cred['name'].title().strip()
                # Busco la coma
                poscoma = autor.find(',')
                # Si hay coma me quedo con lo de la izquierda
                if  poscoma > -1:
                    autor = autor[:poscoma]
                # Saco símbolos extraños
                autor = re.sub('[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]', '', autor).strip()
        loader.add_value('author', autor)
        loader.add_value('title', item['headlines']['basic'])
        loader.add_value('url',
                         'https://www.abc.com.py/' + item['website_url'])
        return loader.load_item()
