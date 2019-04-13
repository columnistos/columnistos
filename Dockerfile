FROM python:3.6
MAINTAINER Lu Pa <admin@tedic.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
        && apt-get install -y \
                sqlite3 \
        && apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir logs

COPY . .

# para poder recueprar su contenido al guardar la persistencia
RUN mv diarios diariosAux

COPY docker-run.sh /

CMD [ "/docker-run.sh" ]
