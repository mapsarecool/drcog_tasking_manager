############################################################
# Dockerfile to build Nginx Installed Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu:18.04

# File Author / Maintainer
MAINTAINER James McAndrew <jim@loc8.us>

# Install Nginx

# Install necessary tools
RUN apt-get update -y && \
    apt-get install -y \
    --no-install-recommends \
      apt-utils \
      cron \
      dialog \
      net-tools \
      nginx \
      software-properties-common

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf
ADD ./conf/nginx.conf /etc/nginx/nginx.conf

# Enable HTTPS
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04
RUN add-apt-repository ppa:certbot/certbot && \
  apt-get update && \
  apt-get install -y \
    python-certbot-nginx \
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

RUN certbot renew

# # Add rendering tasks to CRON
# RUN mkdir -p /etc/cron.d/ && touch /etc/cron.d/renew-task /etc/crontab /etc/cron.*/*
# RUN echo "30 2 10 * * certbot renew >/dev/null 2>> /cron_error_log" > /etc/cron.d/renew-task
# RUN chmod 0644 /etc/cron.d/renew-task
# RUN service cron start

RUN echo "30 2 10 * * certbot renew >/dev/null 2>> /cron_error_log" > /crontasks
RUN echo "#!/bin/bash" > /start.sh
RUN echo "crontab -r" >> /start.sh
RUN echo "cat /crontasks | crontab -" >> /start.sh
RUN echo "crontab -l" >> /start.sh
RUN echo "/etc/init.d/cron restart" >> /start.sh
RUN echo "service nginx start" >> /start.sh
