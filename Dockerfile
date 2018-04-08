FROM python:3
MAINTAINER Lu Pa <admin@tedic.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
        && apt-get install -y \
        sqlite3 \
        && apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN ["chmod", "+x", "runcrawlers_cr.sh" ]

RUN mkdir logs

COPY . .
COPY docker-run.sh /

CMD [ "/docker-run.sh" ]
