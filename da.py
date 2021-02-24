import models


def get_library():
    return list(models.Song.select())


def get_song(id):
    return list(models.Song.selectBy(id=id))[0]


def update_song_lyrics(song, lyrics):
    song.lyrics = lyrics
    song.syncUpdate()
