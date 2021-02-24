import os
import shutil
from bing_image_downloader import downloader
from PIL import Image
import re
import urllib.request
from bs4 import BeautifulSoup


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


def get_lyrics(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    # remove starting 'the' from artist e.g. the who -> who
    if artist.startswith("the"):
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>', '').replace(
            '</br>', '').replace('</div>', '').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" + str(e)
