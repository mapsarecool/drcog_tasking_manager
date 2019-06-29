#!/bin/bash


# Database
#  OSMTM requires a PostgreSQL/PostGIS database. Version 2.3 or higher of
#    PostGIS is required.
#  First create a database user/role named www-data:
psql -c "CREATE USER \"$WWWDATA_USER\" WITH PASSWORD '$WWWDATA_PASSWORD' NOCREATEDB NOSUPERUSER NOCREATEROLE;"

#  Then create a database named osmtm:
psql -c "CREATE DATABASE \"$TM_DB_NAME\" OWNER '$WWWDATA_USER' TEMPLATE template0 ENCODING UTF8;"
psql -d $TM_DB_NAME -c "CREATE EXTENSION postgis;"

cd /osm-tasking-manager2

# Update the production and development ini files
CONNECTION_STRING="postgresql://$WWWDATA_USER:$WWWDATA_PASSWORD\@$PGHOST/$TM_DB_NAME"
perl -p -e "s|postgresql.+|$CONNECTION_STRING|g" -i /osm-tasking-manager2/production.ini
perl -p -e "s|postgresql.+|$CONNECTION_STRING|g" -i /osm-tasking-manager2/development.ini

# Populate the database
#   You're now ready to do the initial population of the database. An
#   initialize_osmtm_db script is available in the virtual env for that:
./env/bin/initialize_osmtm_db
