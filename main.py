from flask import Flask, jsonify, request
from flask_cors import CORS
import waitress
import bl

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


@app.route('/library')
def get_library():
    return jsonify(bl.get_library()), 200


@app.route('/stream')
def get_stream_url():
    song_id = request.args.get('id', None)
    quality = request.args.get('quality', 'high').lower()

    if song_id is not None:
        result = bl.get_stream_url(song_id, quality)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/artists')
def get_artists():
    result = bl.get_artists()
    return jsonify(result), result['code']


@app.route('/lyrics')
def get_lyrics():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.get_lyrics(song_id)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/library/export')
def export_library():
    result = bl.export_library()
    return jsonify(result), result['code']

    
@app.route('/library/import', methods=['POST'])
def import_library():
    playlist_file = request.files.get('file', None)
    if playlist_file is not None:
        result = bl.import_library(playlist_file)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No import file provided'}), 400


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=7474)
