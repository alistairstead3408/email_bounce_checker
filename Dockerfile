FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN ln -sf /bin/bash /bin/sh

CMD python -u server/api.py