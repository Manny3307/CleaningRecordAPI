FROM continuumio/anaconda3

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

ENV PATH=/root/anaconda/bin:$PATH

RUN conda create -n cleaningrecords python=3.9.6
RUN echo "source activate cleaningrecords" > ~/.bashrc
ENV PATH /opt/conda/envs/cleaningrecords/bin:$PATH
RUN python -m pip install --upgrade pip
RUN pip3 install numpy pandas matplotlib seaborn scipy scikit-learn mysql-connector pdfkit sqlalchemy wheel \
         wkhtmltopdf kafka rest-pandas

SHELL ["/bin/bash", "-c"]

FROM python:3.9-alpine3.13

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip3 install -r /requirements.txt

RUN pip3 install psycopg2 websocket-client
RUN pip3 install Pillow boto3
RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter 
RUN apk del .tmp-build-deps

RUN mkdir /cleaningrecord

RUN mkdir /app

COPY ./app /app

WORKDIR /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
RUN chmod -R 755 /cleaningrecord
USER user