import shutil
import os
from bing_image_downloader import downloader
import shutil
import os
import da
import utils

songs = [song.to_dict() for song in da.get_library()]
for song in songs:
    utils.generate_artist_image(song['artist'])
