#!/bin/bash

service apache2 stop
cp /app/flask.conf /etc/apache2/sites-available/flask.conf
a2ensite flask.conf
service apache2 start
tail -f /var/log/apache2/access.log
