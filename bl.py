import da
import youtube_dl
import re
from bing_image_downloader import downloader
import shutil
import os


def get_library():
    return [song.to_dict() for song in da.get_library()]


def get_stream_url(song_id):
    song = da.get_song(song_id)
    if song is not None:
        ydl_opts = {
            'format': 'bestaudio',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song.url, download=False)
            stream_url = info['formats'][0]['url']
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

    yt_id = re.search(
        '((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', url)
    if yt_id is not None:
        art = 'https://i.ytimg.com/vi/' + yt_id.group() + '/maxresdefault.jpg'
    else:
        art = ''

    success = da.add_song(name, artist, url, art, tags)

    if success:
        generate_artist_image(artist)
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
        generate_artist_image(artist)
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
        name = get_valid_filename(song['artist'])
        if name not in artist_names:
            artist_names.append(name)

    result = []
    for name in artist_names:
        result.append({
            'name': name,
            'imagePath': '/artists/' + name
        })

    return {'code': 200, 'results': result}


def generate_artist_image(artist):
    name = get_valid_filename(artist)

    base_save_path = 'static/artists/' + name
    if not os.path.exists(base_save_path):
        downloader.download(
            name, limit=1,  output_dir='bing_download_artists', adult_filter_off=False, force_replace=True, timeout=60)

        base_download_path = 'bing_download_artists/' + name + '/Image_1'
        if os.path.exists(base_path + '.jpg'):
            shutil.copyfile(base_path + '.jpg', base_save_path)
        elif os.path.exists(base_path + '.png'):
            shutil.copyfile(base_path + '.png', base_save_path)
        elif os.path.exists(base_path + '.jpeg'):
            shutil.copyfile(base_path + '.jpeg', base_save_path)
        else:
            pass

    shutil.rmtree('bing_download_artists', ignore_errors=True, onerror=None)


def get_valid_filename(name):
    return name.replace('&', 'and').replace('+', 'and')
