#!/bin/bash

sudo rm /etc/nginx/sites-enabled/default
sudo /bin/ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo service nginx restart
#sudo /bin/ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn restart
sudo apt update
sudo apt remove python-django -y
sudo apt remove gunicorn -y
sudo apt install mc -y
sudo apt install python3-pip -y
sudo apt install python2.7 -y
sudo apt install supervisor -y
sudo pip3 install gunicorn
sudo pip3 install django
sudo cp /home/box/web/etc/supervisord.conf /etc/supervisor/supervisord.conf
sudo ln -s /home/box/web/etc/ask.conf /etc/supervisor/conf.d/ask.conf
sudo service supervisor start
sudo service mysql start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart ask
mysql -u root -e "create database ask"
mysql -u root -e "create user askuser@localhost IDENTIFIED BY 'pass'"
mysql -u root -e "GRANT ALL ON ask.* TO askuser@localhost"
mysql -u root -e "FLUSH PRIVILEGES"