from flask import Flask, Response, request
import get_osm_data

app = Flask(__name__)

# Index
@app.route('/', methods=['GET'])
def app_indexa():
    return 'Hello World'

@app.route('/api', methods=['GET'])
def app_index1():
    return 'Hello World1'

@app.route('/tile/<multi>part/<grid_id>', methods=['GET'])
def load_tile(grid_id, multi):
    mimetype = 'application/vnd.openstreetmap.data+xml'

    # Allow for testing in the browser
    if request.args.get('f') == 'text':
        mimetype = 'text/plain'

    if multi == 'multi':
        return Response(get_osm_data.get_tile_multi_part(grid_id), mimetype=mimetype)
    elif multi == 'single':
        return Response(get_osm_data.get_tile_single_part(grid_id), mimetype=mimetype)
    else:
        return Response('Must use singlepart or multipart', status=404, mimetype='text/plain')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
