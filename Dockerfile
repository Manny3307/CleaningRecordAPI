FROM python:3.11.0a2-alpine3.14

ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user