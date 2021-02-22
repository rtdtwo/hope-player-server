import shutil
import os
from bing_image_downloader import downloader
import shutil
import os

def generate_artist_images():
    songs = [song.to_dict() for song in da.get_library()]
    artist_names = []
    for song in songs:
        name = get_valid_filename(song['artist'])
        if name not in artist_names:
            artist_names.append(name)

        if not os.path.exists('static/artists/' + name + '.jpg'):
            downloader.download(
                name, limit=1,  output_dir='bing_download_artists', adult_filter_off=False, force_replace=True, timeout=60)

            shutil.copyfile('bing_download_artists/' + name + '/Image_1.jpg',
                            'static/artists/' + name + '.jpg')

    shutil.rmtree('bing_download_artists', ignore_errors=True, onerror=None)


def get_valid_filename(name):
    return name.replace('&', 'and').replace('+', 'and')