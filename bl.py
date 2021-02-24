import da
import youtube_dl
import re
import os
import utils
import json
import time


def get_library():
    return {
        'code': 200,
        'results': [song.to_dict() for song in da.get_library()]
    }


def export_library():
    return {
        'code': 200,
        'result': {
            'timestamp': time.time(),
            'library': [song.to_dict() for song in da.get_library()]
        }
    }


def get_stream_url(song_id, quality):
    if quality == 'low':
        quality_index = 0
    elif quality == 'med':
        quality_index = 1
    else:
        quality_index = 2

    song = da.get_song(song_id)
    if song is not None:
        ydl_opts = {
            'format': 'bestaudio'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song.url, download=False)
            while True:
                stream_data = info['formats'][quality_index]
                stream_asr = stream_data['asr']
                if stream_asr is None:
                    if quality_index > 0:
                        quality_index -= 1
                    else:
                        return {
                            'code': 500,
                            'msg': 'No reliable audio streams found for this video.'
                        }
                else:
                    stream_url = stream_data['url']
                    return {
                        'code': 200,
                        'result': stream_url
                    }
    else:
        return {
            'code': 404,
            'msg': 'No such song found'
        }


def add_song(data):
    name = data['name']
    artist = data['artist']
    url = data['url']
    tags = data['tags']

    art = utils.generate_album_art(url)

    success = da.add_song(name, artist, url, art, tags)

    if success:
        utils.generate_artist_image(artist)
        return {
            'code': 201,
            'msg': 'Added successfully'
        }
    else:
        return {
            'code': 500,
            'msg': 'Failed to add'
        }


def delete_song(song_id):
    success = da.delete_song(song_id)
    if success:
        return {
            'code': 200,
            'msg': 'Deleted successfully'
        }
    else:
        return {
            'code': 500,
            'msg': 'Failed to delete'
        }


def edit_song(data):
    song_id = data['id']
    name = data['name']
    artist = data['artist']
    tags = data['tags']

    success = da.edit_song(song_id, name, artist, tags)

    if success:
        utils.generate_artist_image(artist)
        return {
            'code': 200,
            'msg': 'Edited successfully'
        }
    else:
        return {
            'code': 500,
            'msg': 'Failed to edit'
        }


def get_artists():
    songs = [song.to_dict() for song in da.get_library()]
    artist_names = []
    for song in songs:
        name = utils.get_valid_filename(song['artist'])
        if name not in artist_names:
            artist_names.append(name)

    result = []
    for name in artist_names:
        result.append({
            'name': name,
            'imagePath': '/artists/' + name + '.jpg'
        })

    return {'code': 200, 'results': result}


def get_lyrics(song_id):
    song = da.get_song(song_id)
    if song is None:
        return {
            'code': 400,
            'msg': 'No song with ID {} exists'.format(song_id)
        }

    lyrics = song.lyrics
    if lyrics == '':
        lyrics = utils.get_lyrics(song.artist, song.name)
        da.update_song_lyrics(song, lyrics)

    return {
        'code': 200,
        'result': lyrics
    }


def import_library(import_file):
    import_data = json.load(import_file)
    import_library = import_data['library']
    successes = 0
    failures = 0
    for song in import_library:
        try:
            da.add_song(
                song['name'],
                song['artist'],
                song['url'],
                utils.generate_album_art(song['url']),
                song['tags']
            )
            successes += 1
        except:
            failures += 1

    return {
        'code': 200,
        'result': {
            'success': successes,
            'fail': failures
        }
    }


def nuke_library():
    shutil.rmtree('static/artists', ignore_errors=True, onerror=None)
    da.nuke_library()
