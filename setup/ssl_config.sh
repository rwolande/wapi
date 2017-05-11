#!/bin/bash

EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 your.provided.subdomain"
  exit $E_BADARGS
fi

subdomain=$1

if [[ $subdomain != *"."* ]]; then
  echo "Subdomain must have at least one period"
  exit $E_BADARGS
fi

echo "Configuring SSL"

sudo apt-get -y update
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi

sudo apt-get -y install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get -y install python-certbot-apache

sudo certbot --apache -d $subdomain

# temp_dir=$(mktemp -d)
# tmp_conf_begin=$(mktemp)
# curl https://raw.githubusercontent.com/rwolande/wapi/master/setup/000-default.conf.mid > tmp_conf_begin
# sudo cp tmp_conf_begin > /etc/apache2/sites-available/000-default.conf

# echo "Finishing!! (:"
# tmp_conf_end=$(mktemp)
# sudo rm /etc/apache2/sites-available/000-default*
# curl https://raw.githubusercontent.com/rwolande/wapi/master/setup/000-default.conf.end > tmp_conf_end
# sudo cp tmp_conf_end > /etc/apache2/sites-available/000-default.conf
# rm -R ${temp_dir}
# sudo apachectl restart

# echo "Defining Server as Subdomain: ${subdomain}"
# sudo echo -e "\nexport SUBDOMAIN_TITLE=${subdomain}\n" >> /etc/apache2/envvars.wol
# sudo sh -c 'cat /etc/apache2/envvars.wol >> /etc/apache2/envvars'
# source /etc/apache2/envvars
# sudo apachectl restart

echo "Done (:"







#Adjusting WSGi and Environment for subdomain
# echo "Adjusting Environment For Subdomain"

# temp_dir=$(mktemp -d)
# tmp_conf_begin=$(mktemp)
# tmp_conf_end=$(mktemp)
# curl https://raw.githubusercontent.com/rwolande/wapi/master/ssl/000-default.conf.begin > tmp_conf_begin
# curl https://raw.githubusercontent.com/rwolande/wapi/master/ssl/000-default.conf.end > tmp_conf_end
# sudo cp tmp_conf_begin > /etc/apache2/sites-enabled/000-default.conf

# echo "Defining Server as Subdomain: ${subdomain}"
# sudo echo -e "\nexport SUBDOMAIN_TITLE=${subdomain}\n" >> /etc/apache2/envvars.wol
# sudo sh -c 'cat /etc/apache2/envvars.wol >> /etc/apache2/envvars'
# source /etc/apache2/envvars
# sudo apachectl restart

# #Get SSL Certs
# echo "Getting Certs"
# wget https://dl.eff.org/certbot-auto
# chmod a+x certbot-auto
# ./certbot-auto certonly --apache -d $subdomain

# #Clean Up
# echo "Cleaning"
# sudo cp tmp_conf_end > /etc/apache2/sites-enabled/000-default.conf
# rm -R ${temp_dir}
# sudo apachectl restart
# echo "Done (:"