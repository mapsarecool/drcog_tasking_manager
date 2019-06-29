FROM python:2.7-jessie

# Newest version!

RUN  apt-get update \
    && apt-get install -y \
    --no-install-recommends \
        libgeos-c1 \
        libgeos-dev \
        python-software-properties \
        software-properties-common \
        wget \
      && apt-get clean \
      && apt-get autoremove \
    && rm -r /var/lib/apt/lists/*

RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update && \
      apt-get install -y \
        postgresql-client-10 \
        postgresql-common \
      && apt-get clean \
      && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive git://github.com/hotosm/osm-tasking-manager2.git
RUN perl -p -i -e 's/transifex-client/transifex-client==0.12.5/g' /osm-tasking-manager2/setup.py
RUN perl -p -i -e 's/geoalchemy2/geoalchemy2==0.3.0/g' /osm-tasking-manager2/setup.py

WORKDIR /osm-tasking-manager2

RUN easy_install virtualenv
RUN virtualenv --no-site-packages env
RUN ./env/bin/pip install -r requirements.txt
