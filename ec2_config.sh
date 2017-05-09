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
echo "a\n]n\n"
sudo mkdir ~/flask_app ~/dev ~/dev/api ~/dev/api/log
echo "b\n]n\n"
sudo mkdir /var/www/html/flask_app /var/www/html/flask_app/wapi
echo "c\n]n\n"
ln -sT ~/flask_app/wapi /var/www/html/flask_app/wapi
echo "d\n]n\n"
echo "Cloning wapi"

git clone https://github.com/rwolande/wapi ~/flask_app

echo "Done (:" > ~/flask_app/wapi/index.html

echo "Now going tocopy over the wsgi file\n\n\n\n"

sudo cp ~/flask_app/wapi/000-default.conf /etc/apache2/sites-enabled/000-default.conf

sudo apachectl restart

# echo "And now file\n\n\n\n"

# sudo cd ~/flask_app/wapi; sudo 