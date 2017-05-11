#!/bin/bash

#create ec2 instance on aws
	#security group: wapi-default
#create elastic ip to obscure dynamic, referencing above ip
#redirect on namecheap to ec2 public ip

#ssh into new server
#pull this file, run this file with 3 arguments

EXPECTED_ARGS=3
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 db_name db_password domain"
  exit $E_BADARGS
fi

db_name=$1
db_password=$2
domain=$3

#PHASE 1 BEGIN - Install necessary packages
echo "Installing Packages: update, apache2, mod-wsgi, python-pip, libssl-dev, setuptools"

# Uncomment if you don't run the SSL script first
sudo apt-get -y update
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi
sudo apt-get -y install python-pip
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
sudo -H pip install -U setuptools
sudo apt-get -y install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get -y install python-certbot-apache

sudo certbot --apache -d $domain

echo "Installing Packages: libmysqlclient-devm mysql-server"
sudo apt-get -y install libmysqlclient-dev
sudo apt-get -y install mysql-server
sudo mysql_secure_installation
#PHASE 1 COMPLETE

#PHASE 2 BEGIN - Clone wapi & link
echo "Cloning wapi"
mkdir ~/flask_app ~/flask_app/wapi ~/dev ~/dev/wapi ~/dev/wapi/log
git clone https://github.com/rwolande/wapi ~/flask_app/wapi

echo "Creating link"
sudo ln -sT ~/flask_app /var/www/html/flask_app

echo "Installing additional requirements"
cd ~/flask_app/wapi;
sudo pip install -r requirements.txt;
#PHASE 2 COMPLETE

#PHASE 3 BEGIN - Set up environment and database
echo "Configuring Environment Settings"
{
  echo -n $'DB_ENV = \'local\''; echo -e $' #ENVIRONMENT (ENUM)\n'

  echo -n 'MYSQL_DB = '\'${db_name}; echo $'\' #SQL DB NAME'
  echo -n $'MYSQL_HOST = \'localhost\''; echo ' #SQL HOST'
  echo -n $'MYSQL_USER = \'root\''; echo ' #SQL USER'
  echo -n 'MYSQL_PASSWORD = '\'${db_password}; echo -e $'\' #SQL DB PW\n'

  echo -n $'JWT_KEY = \'\''; echo ' #JWT KEY'
  echo -n $'LOG_DIR = \'~/dev/api/log\''; echo ' #LOG DIRECTORY'
} > ~/flask_app/wapi/instance/config.py

echo "Generating basic database from api/sql/create_db script for DB ${db_name}"
sudo ~/flask_app/wapi/api/sql/create_db $db_name

#PHASE 3 COMPLETE

#PHASE 4 BEGIN - Sync

echo "Editing conf files, if this doesnt work fixes should be trivial. Check apache error log in /var/log/apache2/ if no output here but things don't work as expected."

#Edit 000-default.conf adding this

sudo chmod 777 /etc/apache2/sites-enabled
{
  echo -e "\n\tServerName ${domain}"
  echo -e "\n\tWSGIScriptAlias / /var/www/html/flask_app/wapi/wsgi.py";
  echo -e "\n\t<Directory /var/www/html/flask_app/wapi>";
  echo -e "\t\tWSGIApplicationGroup %{GLOBAL}";
  echo -e "\t\tRequire all granted";
  echo -e "\t</Directory>";
} > wol.conf
sed -i "13r wol.conf" /etc/apache2/sites-enabled/000-default.conf
sed -i "13r wol.conf" /etc/apache2/sites-enabled/000-default-le-ssl.conf
sudo apachectl restart





echo "Done (:"