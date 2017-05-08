#!/bin/bash

#Below line should already be ran, 
# cd ~
# mkdir ~/flask_app
# cd ~/flask_app
# git clone https://github.com/rwolande/wapi
# cd wapi

sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install python-pip

sudo -H pip install -U setuptools

sudo apt-get install libmysqlclient-dev
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo mysql_install_db

#sudo pip install flask
#sudo pip install flask_restful
#sudo pip install flask_mysqldb
#sudo pip install jwt

sudo mkdir /var/www/html/flask_app
sudo mkdir /var/www/html/flask_app/wapi
sudo ln -sT ~/flask_app/wapi /var/www/html/flask_app/wapi

echo "Hello World" > ~/flask_app/wapi/index.html