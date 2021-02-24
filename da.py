import models
import time

def get_library():
    return list(models.Song.select())


def get_song(id):
    return list(models.Song.selectBy(id=id))[0]


def update_song_lyrics(song, lyrics):
    song.lyrics = lyrics
    song.syncUpdate()


def add_song(name, artist, url, art, tags):
    try:
        song = models.Song(
            name=name,
            artist=artist,
            url=url,
            art=art,
            lyrics='',
            added=time.time(),
            tags=json.dumps([tag.strip() for tag in tags.split(',')])
        )
        song.set()
        return True, None
    except Exception as e:
        return False, e
