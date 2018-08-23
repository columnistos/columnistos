#!/bin/bash
# Script que hace lo siguiente: 
#   1. Saca los resultados
#   2. Los expone como CSV en la carpeta pub
#
#   OBS: Mantiene un solo archvo que se sobreescribe cada ejecución

# Variables
pais="$1"
carpetascript="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
carpeta="$carpetascript"/public
bincompose=/usr/local/bin/docker-compose

# Controlo que se ingrese al menos 1 parametro
nom_script="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
if [ $# -lt 1 ]; then
    echo -e "\nModo de empleo: $nom_script [país o región]\n"
    exit 1
fi

# creo carpeta por si no existe
mkdir -p $carpeta

# Obtengo resultados
# FIXME: como la base ahora no diferencia país, el nombre del país solo se pide
#         para nombrar al archivo csv
echo -e "Obteniendo resultados"
$bincompose -f $carpetascript/docker-compose.yml run --rm app sqlite3 \
	-header -csv /usr/src/app/diarios/diarios.sqlite \
	"select * from articles a join authors aut where a.author_id = aut.id;" > \
	"$carpeta"/"$pais"-articulos.csv

