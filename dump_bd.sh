#!/bin/bash

# Instrucciones:

# hacer un clone de https://github.com/columnistos/dump en el directorio padre de donde este corriendo columnistos
# subir el ssh key publico del servidor donde corre columnistos a la cuenta de github que quieren usar para hacer los dumps
# pedir a j-e-d o a rusosnith permiso de escritura para la cuenta de github que van a usar para hacer push al repo dump
# reemplazar en el script que sigue los <reemplazar ...> por el código de país que corresponda
# en dump crear la carpeta del código de país
# agregar un cronjob que corra este script una vez por día

sqlite3 -header -csv ./diarios/diarios.sqlite "select * from articles a join authors aut where a.author_id = aut.id;" > ../dump/<reemplazar por iso code del país>/articulos.csv
cd ../dump/
git add <reemplazar por iso code del país>/articulos.csv
git pull origin master
git commit -am "Actualización <reemplazar por iso code del país>/articulos.csv"
git push origin master
