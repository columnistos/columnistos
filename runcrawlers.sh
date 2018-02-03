#!/bin/sh
export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios
scrapy crawl clarin
scrapy crawl lanacion
scrapy crawl pagina12
scrapy crawl perfil
