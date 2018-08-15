#!/bin/bash
cd /home/gabygarro/Documents/columnistos

source venv/bin/activate
pip install -r requirements.txt

export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios
scrapy crawl nacion
scrapy crawl crhoy
scrapy crawl delfino
scrapy crawl larepublica
