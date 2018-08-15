#!/usr/bin/env bash
export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios
scrapy crawl nacion
scrapy crawl crhoy
scrapy crawl delfino
scrapy crawl larepublica
