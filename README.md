# Intro

Código de [@columnistOS]. Idea de [@rusosnith](https://twitter.com/rusosnith), programado originalmente por [@j_e_d](https://twitter.com/j_e_d).

Autores en [COLLABORATORS.md].

PRs bienvenidos.


## En los medios:

[Resumen de 2018 de Columnitos Argentina:](https://distintaslatitudes.net/columnistos-bot-documentar-brecha-de-genero-en-medios-argentinos)

[En Distintas Latitudes:](https://distintaslatitudes.net/columnistos-bot-documentar-brecha-de-genero-en-medios-argentinos)

[En TELAM, la agencia de noticias estatal argentina:](http://www.telam.com.ar/notas/201712/232365-bot-tuiteo-genero-diarios.html)



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

# Dump

En el archivo `dump_db.sh` hay instrucciones para sumar el dump que se genera al repositorio de la organización.

# Cron

Para que todo funcione automaticamente hay que agregar los `.sh` a algún cronjob. En el caso de [@columnistos] la configuración actual es:

```
30 * * * * $HOME/columnistos/runcrawlers.sh
*/15 * * * * $HOME/columnistos/runbotdm.sh
0 10 * * * $HOME/columnistos/runbottweet.sh
5 10 * * * $HOME/columnistos/dump_db.sh
```
# Instalación y uso con Docker

## Instalar y correr el bot

**1.** Copiar el archivo **docker.env-sample** a **docker.env** y agregar los valores deseados, es decir, las claves de la API de twitter y un par de parámetros más.

También copiar **docker-run.sh-sample** a **docker-run.sh** y cambiar los valores de los diarios a escrapear. 

**2.** Levantar el contenedeor (la primer vez va a demorar pues instala todas las dependencias y crea la base de nombres):
```
docker-compose up app
```

Con esto ya se puede poner el scrapper a funcionar, corriendo cada vez: `docker-compose up -d app`

Si se desea comenzar con base nueva, borrar el archivo **diarios.sqlite** que está dentro de la carpeta **diarios** y volver al punto 2

Además esta otra funcionalidad es importante: 

## Mensaje directo

Se utiliza para corregir nombres sin género y otros avisos:

**OBS:** antes de correr este comando se deben configurar los ususarios de twitter en `columnistos_bot.py`

Comando para enviar el mensaje:
```
docker-compose run --rm app python columnistos_bot.py -dm
```

## Tuit

Luego de dos días de correr el bot, **se puede empezar a tuitear**, con este comando:

```
docker-compose run --rm app python columnistos_bot.py -tweet
```

## Exponer los resultados

**1.** Exportar la base a la carpeta `public` en formato csv con este comando:

```
./columnistos-pub.sh PAIS-o-REGION
```

**2.** Publicar la carpeta `public` usando servidor web en el puerto 8095:

```
docker-compose up -d web
```

Esto deja corriendo un **servidor web**, quiere decir que si se apaga la computadora o se hace un `docker-compose stop` la base csv ya no estará públicamente dispinible. 

Para verlo en tu computaodra local, puedes acceder a localhost:8095 en tu navegador. 

## Un ejemplo de CRON con docker para Paraguay:

```
BIN=/usr/local/bin
APP=/carpeta-donde-esta-instalado-el-bot/columnistos-docker
USUARIO=usuario-unix-con-capacidad-de-ejecutar-docker-compose
# Corro el crawler a las 00:01 y DM por si hay algo que corregir
01 00 * * * $USUARIO cd $APP && $BIN/docker-compose up -d app && $BIN/docker-compose run --rm app python columnistos_bot.py -dm
# Publico csv a las 00:20
20 00 * * * $USUARIO cd $APP && ./columnistos-pub.sh paraguay
# Corro el crawler cada 4 horas
0 */4 * * * $USUARIO $BIN/docker-compose -f $APP/docker-compose.yml up -d app
# Twit a las 8:00
0 8 * * * $USUARIO $BIN/docker-compose -f $APP/docker-compose.yml run --rm app python columnistos_bot.py -tweet
```

[@columnistos]: https://twitter.com/columnistos
[COLLABORATORS.md]: COLLABORATORS.md
