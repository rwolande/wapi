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

#Apache Installation
echo "Installing Apache"

sudo apt-get -y install apache2

#Adjusting WSGi and Environment for subdomain
echo "Adjusting Environment For Subdomain"

temp_dir=$(mktemp -d)
tmp_conf_begin=$(mktemp)
tmp_conf_end=$(mktemp)
curl https://raw.githubusercontent.com/rwolande/wapi/master/ssl/000-default.conf.begin > tmp_conf_begin
curl https://raw.githubusercontent.com/rwolande/wapi/master/ssl/000-default.conf.end > tmp_conf_end
sudo cp tmp_conf_begin > /etc/apache2/sites-enabled/000-default.conf

echo "Defining Server as Subdomain: ${subdomain}"
sudo echo -e "\nexport SUBDOMAIN_TITLE=${subdomain}\n" >> /etc/apache2/envvars.wol
sudo sh -c 'cat /etc/apache2/envvars.wol >> /etc/apache2/envvars'
source /etc/apache2/envvars
sudo apachectl restart

#Get SSL Certs
echo "Getting Certs"
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
./certbot-auto certonly --apache -d $subdomain

#Clean Up
echo "Cleaning"
sudo cp tmp_conf_end > /etc/apache2/sites-enabled/000-default.conf
rm -R ${temp_dir}
sudo apachectl restart
echo "Done (:"