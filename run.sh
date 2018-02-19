#!/bin/bash

# Verifico que exista la base sino la creo 
if [ -f /usr/src/app/diarios/diarios.sqlite ]; then
  echo -e "»»»»»»»»»»»»»»»»»»»»»»»"
  echo -e "»» Ya existe la base »»"
  echo -e "»»»»»»»»»»»»»»»»»»»»»»»"
else
  echo -e "»»»»»»»»»»»»»»»»»»»»»»»"
  echo -e "»» Se inicializa base »"
  echo -e "»»»»»»»»»»»»»»»»»»»»»»»"
  cd diarios && scrapy crawl nombres
fi

# Ahora sí corro el crawler
cd /usr/src/app && ./runcrawlers_paraguay.sh
