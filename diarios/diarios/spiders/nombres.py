# -*- coding: utf-8 -*-
import os

import scrapy


class NombresSpider(scrapy.Spider):
    name = 'nombres'
    # parse it from local web server
    cwd = os.getcwd()
    print(cwd)
    start_urls = [f'file:////127.0.0.1/{cwd}/Nombres.html']

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {'diarios.pipelines.StoreNames': 100}
    }

    def parse(self, response):
        for line in response.xpath('//tbody//tr'):
            yield{
                'name': line.xpath('./td[1]/text()').extract()[0],
                'gender': line.xpath('./td[2]/text()').extract()[0]
            }
