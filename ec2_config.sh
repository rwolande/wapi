#!/bin/bash

#Below line should already be ran, 
# cd ~
# mkdir ~/flask_app
# cd ~/flask_app
# git clone https://github.com/rwolande/wapi
# cd wapi

echo "wol Installing basic packages"
echo "wol apt-get update\n"
sudo apt-get update
echo "wol apt-get install apache2"
sudo apt-get install apache2
echo "wol libapache2-mod-wsgi"
sudo apt-get install libapache2-mod-wsgi
echo "wol python-pip"
sudo apt-get install python-pip

echo "wol setuptools"
sudo -H pip install -U setuptools

echo "wol libmysqlclient-dev"
sudo apt-get install libmysqlclient-dev
echo "wol mysql-server"
sudo apt-get install mysql-server
echo "wol secure sql install"
sudo mysql_secure_installation
echo "wol mysql_install_db"
sudo mysql_install_db

#sudo pip install flask
#sudo pip install flask_restful
#sudo pip install flask_mysqldb
#sudo pip install jwt

sudo mkdir ~/flask_app ~/dev ~/dev/api ~/dev/api/log
sudo mkdir /var/www/html/flask_app /var/www/html/flask_app/wapi
ln -sT ~/flask_app/wapi /var/www/html/flask_app/wapi

echo "Cloning wapi"

git clone https://github.com/rwolande/wapi ~/flask_app

echo "Done (:" > ~/flask_app/wapi/index.html

echo "Now go to ~/flask_app/wapi, pip install the requirements, copy over the wsgi file, "

sudo apachectl restart