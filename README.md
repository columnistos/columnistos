# Intro

Código de [@columnistOS]. Idea de [@rusosnith](https://twitter.com/rusosnith), programado originalmente por [@j_e_d](https://twitter.com/j_e_d).

Autores en [COLLABORATORS.md].

PRs bienvenidos.

## Bots Hermanas:

Chile: [@columnistas_cl](https://twitter.com/columnistas_cl).

Colombia: [@LeTengo_elDato](https://twitter.com/LeTengo_elDato).

Costa Rica: [@columnistosCR](https://twitter.com/columnistoscr).

Paraguay: [@TEDICpy](https://twitter.com/TEDICpy).

# Instalación

- Crear un virtualenv de Python 3
```
python3 -m venv ./venv
source venv/bin/activate
```
- Instalar requerimientos
```
pip install -r requirements.txt
```

# Scraping

Esta parte usa [Scrapy](https://scrapy.org).

## Instalando base de nombres:

```
cd diarios
scrapy crawl nombres
```

Esto corre el scraper que está en [`./diarios/diarios/spiders/nombres.py`](diarios/diarios/spiders/nombres.py) que lee el archivo [`./diarios/Nombres.html`](diarios/Nombres.html). Este archivo es una copia de la página del [Registro Civil de la Ciudad de Buenos Aires](http://www.buenosaires.gob.ar/areas/registrocivil/nombres/busqueda/buscador_nombres.php?menu_id=16082) donde está el listado de nombres validos y el genero asociado a cada uno de esos nombres.

En la base la columna genero tiene una M para varones, F para mujeres y A para los que se consideran ambiguos, en esos casos el Registro Civil obliga a poner otro nombre que no sea ambiguo.

La mayoría de los nombres de está base no tienen tilde, algunos pocos si. Cuando se comparan los nombres que se obtienen de los medios se les quitan los tildes al nombre del que firma y al de la base.

El algoritmo que determina el genero en base al nombre solo considera primer nombre.

Una vez que el scraper de nombres termina debería crear una base `diarios.sqlite` en la carpeta [`./diarios`](diarios/) desde donde se corrió el comando.

Por el momento esa base solo va a tener la tabla `names`.

Este paso es necesario unicamente al instalar.


## Scraping de los diarios:

Para los diarios de Argentina:

```
./runcrawlers.sh
```

Para los diarios de Chile:
```
./runcrawlers_chile.sh
```

Para los diarios de Paraguay:
```
./runcrawlers_paraguay.sh
```

En la carpeta [`./diarios/diarios/spiders/`](diarios/diarios/spiders/) aparte del scaper de nombres hay sub carpetas que agrupan los scrapers por país. En `/ar` están los medios argentinos que por el momento sigue [@columnistos]. En `/cl` hay scrapers para medios chilenos.

El scraper de Clarín (clarin.py) es distinto a los demas por que la página principal de ese diario no carga por completo cuando se pide el home, hay que cargar el resto de la página pidiendo algunos json adicionales.

Para cada scraper se tiene que analizar la página buscando lo que consideramos columnas de opinión y usando selectores xpath o css pasar a `DiariosItem` el titulo, el autor y el url.

En [`./diarios/diarios/pipelines.py`](diarios/diarios/pipelines.py) está el código que procesa los items que se encuentan en cada medio.

En la base se va a crear una table `articles` para los artículos y otra `authors` con nombres completos de autores. Cada articulo tiene un autor asociado. En la tabla `authors` se indica el genero en base a lo que se encontró en la tabla `names` del paso anterior. Los que en este paso queden sin un genero definido son los que se enviaran por DM.


# Twitter

Para lo que sigue se necesitas crear una nueva cuenta de Twitter desde la cuál van a mandar los mensajes y crear una app para que esa cuenta tenga permisos para usar la API de Twitter. Usando la nueva cuenta ir a [apps.twitter.com](https://apps.twitter.com/), habilitar la opción de mandaar DMs para la aplicación. Necesitan copiar algunos valores de esta página para poder completar en los `.sh` las variables:

```
export TWITTER_CONSUMER_KEY=""
export TWITTER_CONSUMER_SECRET=""
export TWITTER_ACCESS_TOKEN=""
export TWITTER_ACCESS_TOKEN_SECRET=""

```

## Mandar y chequear DMs

Esto es para los casos en que no se puede determinar el genero de autores, se pide ayuda a una o varias personas.

Cada vez que corre revisa si hay autores con genero indeterminado, si hay manda un DM a la cuenta que se indique en el código con la consulta del genero. Cada vez que corre también se fija si recibió alguna respuesta y en caso de que suceda intenta procesarla.

Si se envia a más de una persona y las respuestas no coinciden la cuenta bot les informa que eso sucedió para que se pongan de acuerdo y definan.

```
runbotdm.sh
```

## Mandar informe diario

Este es el paso que genera los tweets del resumen del día anterior al que se corre y los tweets de cada medio en caso de que se cumplan ciertas condiciones.

```
runbottweet.sh
```

# Cron

Para que todo funcione automaticamente hay que agregar los `.sh` a algún cronjob. En el caso de [@columnistos] la configuración actual es:

```
30 * * * * $HOME/columnistos/runcrawlers.sh
*/15 * * * * $HOME/columnistos/runbotdm.sh
0 10 * * * $HOME/columnistos/runbottweet.sh
```
# Instalación y uso con Docker

**1.** Copiar el archivo **docker.env-sample** a **docker.env** y agregar los valores deseados. También copiar **docker-run.sh-sample** a **docker-run.sh** y cambiar los valores de los crawls según el país. 

**2.** Correr la instalación (si es que no hay base) y el crawler:
```
docker-compose up
```

**3.** Correr el dm
```
docker-compose run app python columnistos_bot.py -dm
```

**4.** Correr el tweet
```
docker-compose run app python columnistos_bot.py -tweet
```
Si se desea comenzar con base nueva, borrar diarios/diarios.sqlite y volver al punto 2

[@columnistos]: https://twitter.com/columnistos
[COLLABORATORS.md]: COLLABORATORS.md
