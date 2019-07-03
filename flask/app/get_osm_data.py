from osgeo import ogr
from shapely import wkb
import json
import os
import psycopg2
import subprocess
import tempfile
import tilebelt

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
    rooftop.roofprints_osm_final roofprints
WHERE
    (roofprints.building_part IS NOT NULL) = %(get_multipart)s AND
    grid_ref_1000m = (%(grid_y)s || '_' ||  %(grid_x)s)
'''

quad_query = '''
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
    rooftop.roofprints_osm_final roofprints
WHERE
    (roofprints.building_part IS NOT NULL) = %(get_multipart)s AND
    geom_4326 && ST_MakeEnvelope(%(xmin)s, %(ymin)s, %(xmax)s, %(ymax)s, 4326)
'''

def get_tile(query_type, params):
    # Query the Database
    params['get_multipart'] = params['multi'] == 'multi'
    if query_type == 'grid':
        obj = query_db(grid_query, params)
    elif query_type == 'quadkey':
        params['bbox'] = tilebelt.tile_to_bbox(tilebelt.quadkey_to_tile(params['quadkey']))
        params['xmin'] = params['bbox'][0]
        params['ymin'] = params['bbox'][1]
        params['xmax'] = params['bbox'][2]
        params['ymax'] = params['bbox'][3]
        obj = query_db(quad_query, params)

    geom_column = 'geom_4326'

    # Create a geojson file
    geojson = {'type': 'FeatureCollection', 'features': []}
    for row in obj['rows']:
        geojson_wrapper = {'type': 'Feature', 'properties': {}, 'geometry': {}}
        for i, column in enumerate(obj['description']):
            if column.name != geom_column:
                geojson_wrapper['properties'][column.name] = row[i]
            else:
                as_wkb = wkb.loads(row[i], hex=True)
                as_geojson = ogr.CreateGeometryFromWkb(
                    wkb.dumps(as_wkb)).ExportToJson()
                geojson_wrapper['geometry'] = json.loads(as_geojson)
        geojson['features'].append(geojson_wrapper)

    # Create a file for ogr2osm to use
    #  (ogr2osm requires an output file, so we use a temp one)
    outfile_temp = tempfile.NamedTemporaryFile()

    # Create the command for ogr2osm
    commandline = ('python3', '/ogr2osm/ogr2osm.py', '-t',
                   '/app/drcog_building_trans_pg.py', '/vsistdin/', '-o', outfile_temp.name, '-f')

    # Run ogr2osm
    process = subprocess.Popen(
        commandline, stdin=subprocess.PIPE, encoding='utf8')
    process.communicate(json.dumps(geojson))

    # Read the ogr2osm output into a variable
    osm_data = outfile_temp.read()

    # Close and remove the temp file
    outfile_temp.close()

    # Return the osm
    return osm_data
