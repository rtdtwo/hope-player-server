import models
import time


def get_library():
    return list(models.Song.select())


def get_song(id):
    return list(models.Song.selectBy(id=id))[0]


def add_song(name, artist, url, art, tags):
    try:
        song = models.Song(
            name=name,
            artist=artist,
            url=url,
            art=art,
            added=time.time()
            tags=[tag.strip() for tag in tags.split(',')]
        )
        song.set()
        return True
    except:
        return False


def delete_song(song_id):
    try:
        song = get_song(song_id)
        song.delete()
        return True
    except:
        return False
