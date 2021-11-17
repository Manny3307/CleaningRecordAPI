FROM python:3.11.0a2-alpine3.14

ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN pip3 install psycopg2
RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter 
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user