#!/bin/bash
# Script que hace lo siguiente: 
#   1. Saca los resultados
#   2. Los expone como CSV en la carpeta pub
#
#   OBS: Mantiene un solo archvo que se sobreescribe cada ejecución

# Variables
pais=paraguay
carpetascript="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
carpeta=$carpetascript/public
bincompose=/usr/local/bin/docker-compose

# creo carpeta por si no existe
mkdir -p $carpeta

# Obtengo resultados
echo -e "Sacando resultados"
$bincompose -f $carpetascript/docker-compose.yml run --rm app sqlite3 \
	-header -csv /usr/src/app/diarios/diarios.sqlite \
	"select * from articles a join authors aut where a.author_id = aut.id;" > \
	$carpeta/$pais-articulos.csv

