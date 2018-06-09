#!/bin/sh
export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios
scrapy crawl elmercurio
scrapy crawl latercera
scrapy crawl t13
scrapy crawl eldinamo
scrapy crawl elmostrador
scrapy crawl cooperativa
scrapy crawl theclinic
