#!/bin/bash
sudo -u postgres psql -c "CREATE DATABASE product"
sudo -u postgres psql -c "\c product"
#sudo -u postgres psql product < /vagrant/product_table.sql
sudo -u postgres psql postgres -f /vagrant/product_table.sql
sudo -u postgres psql -c "\copy product FROM '/vagrant/dummy.csv'  DELIMITER ',' CSV HEADER;"