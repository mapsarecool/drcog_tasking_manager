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


def load_tile(table, query, args):
    mimetype = 'application/vnd.openstreetmap.data+xml'

    # Allow for testing in the browser
    if args.get('f') == 'text':
        mimetype = 'text/plain'

    if query['multi'] == 'multi ' or query['multi'] == 'single':
        response = Response(get_osm_data.get_tile(
            table, query),   mimetype=mimetype)
    else:
        response = Response('Must use singlepart or multipart',
                            status=404, mimetype='text/plain')

    return response


@app.route('/quadkey/<multi>part/drcog_<quadkey>.osm', methods=['GET'])
def load_quad(quadkey, multi):
    return load_tile('quadkey', {'quadkey': quadkey, 'multi': multi},
                     request.args)


@app.route('/tile/<multi>part/<int:grid_y>_<int:grid_x>', methods=['GET'])
@app.route('/tile/<multi>part/<int:grid_y>_<int:grid_x>.osm', methods=['GET'])
@app.route('/tile/<multi>part/drcog_<int:grid_y>_<int:grid_x>.osm', methods=['GET'])
def load_grid(grid_x, grid_y, multi):
    return load_tile('grid', {'grid_x': grid_x, 'grid_y': grid_y, 'multi': multi},
                     request.args)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
