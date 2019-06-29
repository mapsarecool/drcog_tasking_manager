FROM ubuntu:18.04

MAINTAINER James McAndrew <jim@loc8.us>

RUN apt-get update -y && \
    apt-get install -y \
    --no-install-recommends \
      software-properties-common

RUN add-apt-repository ppa:ubuntugis/ppa && \
    apt-get update -y && \
    apt-get install -y \
    --no-install-recommends \
      apache2 \
      build-essential \
      gdal-bin \
      git \
      libapache2-mod-wsgi-py3 \
      libgdal-dev \
      python3 \
      python3-dev \
      python3-gdal \
      python3-lxml \
      python3-numpy \
      python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -r /var/lib/apt/lists/*

# Set up the Apache server
RUN a2enmod wsgi
RUN service apache2 restart

# Add our app to /var/www
RUN mkdir -p /app/
RUN ln -s /var/www/flask/ /app/

# Set up variables for gdal to compile
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install ogr2osm
RUN git clone --recursive https://github.com/pnorman/ogr2osm
WORKDIR /ogr2osm
RUN git pull
RUN git submodule update

# Install our flask program
COPY ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN python3 -m pip install setuptools
RUN python3 -m pip install -r requirements.txt
