import os
import shutil
from bing_image_downloader import downloader
from PIL import Image
import lyricsgenius
import re


def generate_artist_image(artist):
    name = get_valid_filename(artist)

    base_download_root = 'bing_download_artists'
    base_save_path = 'static/artists'
    base_save_file = base_save_path + '/' + name + '.jpg'

    if not os.path.exists(base_save_file):
        search_term = name + ' music artist'
        downloader.download(
            search_term, limit=1,  output_dir=base_download_root, adult_filter_off=False, force_replace=True, timeout=60)

        base_download_path = base_download_root + '/' + search_term
        base_download_image = os.listdir(base_download_path)[0]

        cropped = crop_image(base_download_path + '/' + base_download_image)
        rgb_image = cropped.convert('RGB')
        resized_image = rgb_image.resize((400, 400))
        resized_image.save(base_save_file)

    shutil.rmtree(base_download_root, ignore_errors=True, onerror=None)


def get_valid_filename(name):
    return name.replace('&', 'and').replace('+', 'and'). replace(',', ' and')


def crop_image(image_path):
    image = Image.open(image_path)
    img_width, img_height = image.size

    top_x = 0
    top_y = 0
    bottom_x = 0
    bottom_y = 0

    if img_width > img_height:
        # Landscape
        top_x = (img_width - img_height) / 2
        top_y = 0
        bottom_x = top_x + img_height
        bottom_y = img_height
    else:
        # Portrait
        top_x = 0
        top_y = 0
        bottom_x = img_width
        bottom_y = img_width

    return image.crop((top_x, top_y, bottom_x, bottom_y))


def get_lyrics(artist, title):
    genius = lyricsgenius.Genius()
    song = genius.search_song(title, artist)
    if song is not None:
        return song.lyrics
    
    return None


def generate_album_art(yt_url):
    yt_id = re.search(
        '((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', yt_url)
    if yt_id is not None:
        return 'https://i.ytimg.com/vi/' + yt_id.group() + '/maxresdefault.jpg'
    else:
        return ''