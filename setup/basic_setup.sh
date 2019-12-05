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
#PHASE 1 COMPLETE

#PHASE 2 BEGIN - Clone wapi & link
echo "Cloning wapi"
mkdir ~/flask_app ~/flask_app/api ~/dev ~/dev/site ~/dev/site/log
git clone https://github.com/rwolande/wapi ~/flask_app/api

echo "Creating link"
sudo ln -sT ~/flask_app /var/www/html/flask_app

echo "Installing additional requirements"
cd ~/flask_app/site;
sudo pip install -r requirements.txt;
mkdir instance;
#PHASE 2 COMPLETE

#PHASE 3 BEGIN - Set up environment and database
echo "Configuring Environment Settings"
{
  echo -n $'DB_ENV = \'local\''; echo -e $' #ENVIRONMENT (ENUM)\n'

  echo -n $'JWT_KEY = \'\''; echo ' #JWT KEY'
  echo -n $'LOG_DIR = \'~/dev/api/log\''; echo ' #LOG DIRECTORY'
} > ~/flask_app/site/instance/config.py

#PHASE 3 COMPLETE

#PHASE 4 BEGIN - Sync

echo "Editing conf files, if this doesnt work fixes should be trivial. Check apache error log in /var/log/apache2/ if no output here but things don't work as expected."

#Edit 000-default.conf adding this

sudo chmod 777 /etc/apache2/sites-enabled
{
  echo -e "\n\tServerName ${domain}"
  echo -e "\n\tWSGIScriptAlias / /var/www/html/flask_app/site/wsgi.py";
  echo -e "\n\t<Directory /var/www/html/flask_app/site>";
  echo -e "\t\tWSGIApplicationGroup %{GLOBAL}";
  echo -e "\t\tRequire all granted";
  echo -e "\t</Directory>";
} > wol.conf
sed -i "13r wol.conf" /etc/apache2/sites-enabled/000-default.conf
sed -i "13r wol.conf" /etc/apache2/sites-enabled/000-default-le-ssl.conf
sudo apachectl restart


echo "Done (:"