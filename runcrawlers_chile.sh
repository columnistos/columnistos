#!/bin/sh
export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios
scrapy crawl elmercurio
