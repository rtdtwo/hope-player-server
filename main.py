from flask import Flask, jsonify, request
from flask_cors import CORS
import waitress
import bl

app = Flask(__name__)
CORS(app)


@app.route('/library')
def get_library():
    return jsonify(bl.get_library()), 200


@app.route('/stream')
def get_stream_url():
    song_id = request.args.get('id', None)
    if song_id is not None:
        result = bl.get_stream_url(song_id)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No Song ID provided'}), 400


@app.route('/add', methods=['POST'])
def add_song():
    data = request.json
    if data is not None:
        result = bl.add_song(data)
        return jsonify(result), result['code']
    else:
        return jsonify({'code': 400, 'msg': 'No data provided'}), 400


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=7474)
