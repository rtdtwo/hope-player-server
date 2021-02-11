import models
import time


def get_library():
    return list(models.Song.select())


def get_song(id):
    return list(models.Song.selectBy(id=id))[0]


def add_song(name, artist, url, art):
    try:
        song = models.Song(
            name=name,
            artist=artist,
            url=url,
            art=art,
            added=time.time()
        )
        song.set()
        return True
    except:
        return False
