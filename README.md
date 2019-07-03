# drcog_tasking_manager

Copy `tm.env.example' to 'tm.env' and fill in the variables

## Flask

### Common flask URLS

https://<domain>/api/quadkey/singlepart/drcog_<quadkey>.osm
https://<domain>/api/tile/singlepart/drcog_<grid_row>_<grid_column>.osm

### You can also use:

https://<domain>/api/tile/singlepart/<grid_row>_<grid_column>.osm
https://<domain>/api/tile/singlepart/<grid_row>_<grid_column>

### Using ?f=text will return the OSM data as text
https://<domain>/api/tile/singlepart/<grid_row>_<grid_column>?f=text
