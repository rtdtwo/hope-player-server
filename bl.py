import da
import youtube_dl
import re


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
        return {
            'code': 200,
            'msg': 'Edited successfully'
        }
    else:
        return {
            'code': 500,
            'msg': 'Failed to edit'
        }