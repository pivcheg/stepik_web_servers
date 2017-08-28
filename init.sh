#!/bin/bash

sudo rm /etc/nginx/sites-enabled/default
sudo /bin/ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
#sudo /bin/ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn restart
#﻿sudo /etc/init.d/mysql restart﻿
sudo apt update
sudo apt remove python-django -y
sudo apt remove gunicorn -y
sudo apt install mc -y
sudo apt install python3-pip -y
sudo apt install python2.7 -y
sudo apt install supervisor -y
sudo pip3 install gunicorn
sudo pip3 install django
sudo cp /home/box/web/etc/supervisord.conf /etc/supervisor/supervisord.conf -y
sudo ln -s /home/box/web/etc/ask.conf /etc/supervisor/conf.d/ask.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart ask
