# Instalación
- Crear un virtualenv de Python 3
- Instalar requerimientos
```
pip install -r requirements.txt
```

# Scraping
Esta parte usa Scrapy para funcionar

## Instalando base de nombres:

```
cd diarios
scrapy crawl nombres
```

Esto corre el scraper que está en `./diarios/diarios/spiders/nombres.py` que lee el archivo `./diarios/Nombres.html`. Este archivo es una copia de la [página](http://www.buenosaires.gob.ar/areas/registrocivil/nombres/busqueda/buscador_nombres.php?menu_id=16082) del Registro Civil de la Ciudad de Buenos Aires donde está el listado de nombres validos y el genero asociado a cada uno de esos nombres.

En la base la columna genero tiene una M para varones, F para mujeres y A para los que se consideran ambiguos, en esos casos el Registro Civil obliga a poner otro nombre que no sea ambiguo.
La mayoría de los nombres de está base no tienen tilde, algunos pocos si. Cuando se comparan los nombres que se obtienen de los medios se les quitan los tildes al nombre del que firma y al de la base.
El algoritmo que determina el genero en base al nombre solo considera primer nombre por el momento ya qu no siempre se puede determinar si lo que sigue son otros nombres o el apellido.

Una vez que el scraper de nombres termina debería crear una base `diarios.sqlite` en la carpeta `./diarios` desde donde se corrió el comando. 
Por el momento esa base solo va a tener la tabla `names`.

## Scraping de los diarios:

```
runcrawlers.sh
```

En la carpeta `./diarios/diarios/spiders/` aparte del scaper de nombres hay 4 scrapers para los medios argentinos que por el momento sigue @columnistos.
El scaper de Clarín (clarin.py) es distinto a los demas por que la página principal de ese diario no carga por completo cuando se pide el home, hay que cargar el resto de la página pidiendo algunos json adicionales.
Para cada scraper se tiene que analizar la página buscando lo que consideramos columnas de opinión y usando selectores xpath o css pasar a `DiariosItem` el titulo, el autor y el url.
En `./diarios/diarios/pipelines.py` está el código que procesa los items que se encuentan en cada medio.  

# Twitter
Para lo que sigue se necesitas una cuenta de Twitter para el bot con permisos para usar la API de Twitter

## Mandar y chequear DMs 

Esto es para los casos en que no se puede determinar el genero de autores, se pide ayuda a una o varias personas.

```
runbotdm.sh
```

## Mandar informe diario

```
runbottweet.sh
```

# Cron
Para que todo funcione automaticamente hay que agregar los `.sh` a algún cronjob.


