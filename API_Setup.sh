#!/bin/bash
echo "Setting up the Environment for API"
sudo apt-get update
echo "Creating conda environemnt for the API...."
conda create -n apirecords python=3.9.6 -y
echo "Activating conda environment....."
eval "$(conda shell.bash hook)"
conda activate apirecords
echo "Setting up pip...."
python -m pip install --upgrade pip
pip install --upgrade setuptools -y
sudo apt update && apt install -y wkhtmltopdf
echo "Setting up and installing mysql Client"
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential -y
sudo apt-get install python3-bs4 -y
sudo apt-get install libmagickwand-dev -y
pip install mysqlclient
echo "Setting and installing required packages"
pip install rest-pandas django djangorestframework markdown pymysql numpy pandas matplotlib seaborn mysql-connector pdfkit sqlalchemy wheel kafka-python cryptography docker boto3 confluent-kafka pdftotree
pip install -r ./requirements_1.txt
echo "Installing Nginx and doing necessary settings"
sudo apt install nginx -y
sudo ufw allow 'Nginx HTTP'
sudo systemctl enable nginx
sudo systemctl start nginx
sudo cp -i ./nginx/default.conf /etc/nginx/conf.d/default.conf -y
echo "Creating folder to store the cleaning records and giving access to it"
sudo mkdir /cleaningrecord
sudo chmod -R 755 /cleaningrecord
echo "Starting the Gunicorn Server"
sh entrypoint.sh