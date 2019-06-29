#!/bin/bash
if [[ $1 == "" ]]; then
  MODE=development
else
  MODE=$1
fi

echo "Starting tasking manager in $MODE mode"
# Update the production and development ini files
CONNECTION_STRING="postgresql://$WWWDATA_USER:$WWWDATA_PASSWORD\@$PGHOST/$TM_DB_NAME"
USER_DETAILS_URL="https://api.openstreetmap.org/api/0.6/user/details"

perl -p -e "s|postgresql.+|$CONNECTION_STRING|g" -i /osm-tasking-manager2/$MODE.ini

perl -p -e "s|(USER_DETAILS_URL = ).+|\1'$USER_DETAILS_URL'|g" -i /osm-tasking-manager2/osmtm/views/osmauth.py
perl -p -e "s|(CONSUMER_KEY = ).+|\1'$TM_CONSUMER_KEY'|g" -i /osm-tasking-manager2/osmtm/views/osmauth.py
perl -p -e "s|(CONSUMER_SECRET = ).+|\1'$TM_CONSUMER_SECRET'|g" -i /osm-tasking-manager2/osmtm/views/osmauth.py

/osm-tasking-manager2/env/bin/pserve --reload /osm-tasking-manager2/$MODE.ini
