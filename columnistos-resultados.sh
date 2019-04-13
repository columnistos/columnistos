#!/bin/bash
# Script que saca los resultados y opcionalmente lo copia a una carpeta remota dav
# NOTA: para que esto funcion hay que instalar davfs y configurar las credenciales

# Variables
carpetascript="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
carpeta=$carpetascript/columnistos-resultados
subir=n

# Obtengo resultados
echo -e "Sacando resultados"
docker-compose -f $carpetascript/docker-compose.yml run --rm app sqlite3 \
	-header -csv /usr/src/app/diarios/diarios.sqlite \
	"select * from articles a join authors aut where a.author_id = aut.id;" > \
	$carpetascript/$(date +%Y%m%d_%H)_articulos.csv

# Subimos?
echo -e "------------------------------------------------"
echo -n "Desea subir el resultado a davfs (s/n): "
read subir
echo -e "------------------------------------------------"
if [ "$subir" = "s" ]; then

  # Creo carpeta para montar davfs
  mkdir -p $carpeta || exit

  # Monto carpeta remota
  echo -e "Montando carpeta remota"
  sudo mount -t davfs https://nube.tedic.net/remote.php/webdav/TEDIC/ColumnistosResultados $carpeta/
  sudo chown lupa:lupa $carpeta

  # Copio y limpio
  echo -e "Subiendo..."
  mv $carpetascript/$(date +%Y%m%d_%H)_articulos.csv $carpeta
  docker cp columnistosdocker_app_1:/usr/src/app/diarios/diarios.sqlite $carpeta/$(date +%Y%m%d_%H)_diarios.sqlite
  sleep 1

  #Desmonto carpeta
  echo -e "Desmontando carpeta remota"
  sudo umount $carpeta/

  #Limpiamos carpeta
  sleep 1
  # FIXME: verificar si existe y sacar mensaje
  rmdir $carpeta
else
  echo -e "\nNo se copia remotamente, el archivo está en:"
  ls -lh $carpetascript/$(date +%Y%m%d_%H)_articulos.csv
  sleep 2
fi
