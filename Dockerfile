FROM python:3
MAINTAINER Lu Pa <admin@tedic.org>

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir logs

COPY . .
COPY docker-run.sh /

CMD [ "/docker-run.sh" ]
