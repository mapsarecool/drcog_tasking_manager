import json
import os
import subprocess
import psycopg2
from osgeo import ogr
from shapely import wkb
import tempfile

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (
    os.environ['PGHOST'], os.environ['DRCOG_DB'], os.environ['PGUSER'], os.environ['PGPASSWORD'])


def query_db(query, params):
    result = None
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = {
            'error': None,
            'description': cursor.description,
            'rows': cursor.fetchall()
        }
    except (Exception) as e:
        result = {'error': str(e)}
    finally:
        if conn is not None:
            conn.close()
        return result

grid_query = '''
SELECT
    roofprints.bldg_type,
    roofprints.housenumbr,
    roofprints.city,
    roofprints.street,
    roofprints.state,
    roofprints.zip,
    roofprints.bldg_ht_m,
    roofprints.geom_4326
FROM
    rooftop.roofprints_osm_final roofprints JOIN
        rooftop.grid_1000_4326 grid ON
            ST_Contains(grid.geom, roofprints.geom_4326)
WHERE
    (roofprints.building_part IS NULL) = %(get_multipart)s AND
    grid.grid_row || '_' || grid.grid_colum = %(grid_id)s;
'''


def get_tile_multi_part(id):
    return get_tile(id, False)

def get_tile_single_part(id):
    return get_tile(id, True)

def get_tile(id, get_multipart):
    # Query the Database
    obj = query_db(grid_query, {'grid_id': id, 'get_multipart': get_multipart})
    geom_column = 'geom_4326'

    # Create a geojson file
    geojson = {'type': 'FeatureCollection', 'features': []}
    for row in obj['rows']:
        geojson_wrapper = {'type':'Feature','properties':{},'geometry':{}}
        for i, column in enumerate(obj['description']):
            if column.name != geom_column:
                geojson_wrapper['properties'][column.name] = row[i]
            else:
                as_wkb = wkb.loads(row[i], hex=True)
                as_geojson = ogr.CreateGeometryFromWkb(wkb.dumps(as_wkb)).ExportToJson()
                geojson_wrapper['geometry'] = json.loads(as_geojson)
        geojson['features'].append(geojson_wrapper)

    # Create a file for ogr2osm to use
    #  (ogr2osm requires an output file, so we use a temp one)
    outfile_temp = tempfile.NamedTemporaryFile()

    # Create the command for ogr2osm
    commandline = ('python3','/ogr2osm/ogr2osm.py', '-t', '/app/drcog_building_trans_pg.py', '/vsistdin/', '-o', outfile_temp.name, '-f')

    #Run ogr2osm
    process = subprocess.Popen(commandline, stdin=subprocess.PIPE, encoding='utf8')
    process.communicate(json.dumps(geojson))

    #Read the ogr2osm output into a variable
    osm_data = outfile_temp.read()

    #Close and remove the temp file
    outfile_temp.close()

    #Return the osm
    return osm_data
