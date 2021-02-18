import models
import time
import json


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
            added=time.time(),
            tags=json.dumps([tag.strip() for tag in tags.split(',')])
        )
        song.set()
        return True
    except:
        return False


def delete_song(song_id):
    try:
        song = get_song(song_id)
        song.delete(id=song_id)
        return True
    except Exception as e:
        print(e)
        return False


def edit_song(id, name, artist, tags):
    song = get_song(id)

    if song is not None:
        song.name = name
        song.artist = artist
        song.tags = json.dumps([tag.strip() for tag in tags.split(',')])

        song.syncUpdate()

        return True
    else:
        return False