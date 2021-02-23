import shutil
import os
from bing_image_downloader import downloader
import shutil
import os
import da
import utils

songs = [song.to_dict() for song in da.get_library()]
artists = ['Taylor Swift', 'Linkin Park', 'John Williams', 'Queen', 'Shaun Mendes, Justin Bieber']
for artist in artists:
    utils.generate_artist_image(artist)
