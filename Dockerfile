FROM continuumio/anaconda3:latest
USER root
RUN apt-get update -y; apt-get upgrade -y; apt-get install -y vim-tiny vim-athena ssh default-mysql-client
#RUN apt-get -y update && apt-get -y install nginx
ENV PYTHONUNBUFFERED 1

EXPOSE 8080

ENV PATH=/root/anaconda3/bin:$PATH
RUN conda create -n cleaningrecords python=3.9.6
RUN echo "source activate cleaningrecords" > ~/.bashrc
ENV PATH /opt/conda/envs/cleaningrecords/bin:$PATH
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt update && apt install -y wkhtmltopdf
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y
RUN apt-get install python3-bs4 -y
RUN apt-get install libmagickwand-dev -y
RUN pip install mysqlclient
RUN pip install rest-pandas django djangorestframework markdown pymysql numpy pandas matplotlib seaborn \
                 mysql-connector pdfkit sqlalchemy wheel kafka-python cryptography docker boto3 confluent-kafka pdftotree

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

SHELL ["/bin/sh", "-c"]

RUN mkdir /cleaningrecord

RUN mkdir /app

COPY ./app /app
COPY ./entrypoint.sh /

WORKDIR /app

RUN chmod -R 755 /cleaningrecord
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser --disabled-login user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
RUN chmod -R 755 /cleaningrecord
USER root
ENTRYPOINT ["./entrypoint.sh"]