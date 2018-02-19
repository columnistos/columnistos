FROM python:3
MAINTAINER Lu Pa <admin@tedic.org>

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY run.sh /

CMD [ "/run.sh" ]
#CMD [ "python", "./runcrawlers_paraguay.sh" ]
