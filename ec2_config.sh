#!/bin/bash

sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi

sudo apt-get install python-pip
sudo pip install flask

mkdir ~/flask_app
cd ~/flask_app
git clone https://github.com/rwolande/api
sudo ln -sT ~/flask_app/wapi /var/www/html/flask_app/wapi

echo "Hello World" > ~/flask_app/wapi/index.html