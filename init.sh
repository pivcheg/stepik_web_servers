#!/bin/bash

sudo rm /etc/nginx/sites-enabled/default
sudo /bin/ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
#sudo /bin/ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn restart
#﻿sudo /etc/init.d/mysql restart﻿
sudo apt remove python-django
sudo apt remove gunicorn
sudo apt install python3-pip
sudo pip3 install gunicorn
sudo apt install supervisor
sudo ln -s /home/box/web/etc/supervisor.conf /etc/supervisor/conf.d/ask.conf
