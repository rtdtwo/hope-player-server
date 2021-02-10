import da
import youtube_dl


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
            print(stream_url)
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

    success = da.add_song(name, artist, url)

    if success:
        return {
            'code': 201,
            'msg': 'Added successfully'
        }
    else:
        return {
            'code': 501,
            'msg': 'Failed to add'
        }
