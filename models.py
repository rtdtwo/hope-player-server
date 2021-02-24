import os
import json
from sqlobject import SQLObject, sqlhub, connectionForURI, StringCol, BigIntCol
import sqlite3

connection_string = os.environ['DATABASE_URL']
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection


class Song(SQLObject):
    name = StringCol()
    artist = StringCol()
    art = StringCol()
    url = StringCol()
    added = BigIntCol()
    tags = StringCol()
    lyrics = StringCol()

    def to_dict(self):
        if self.tags == '':
            tags = []
        else:
            tags = json.loads(self.tags)

        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'art': self.art,
            'added': self.added,
            'url': self.url,
            'lyrics': self.lyrics,
            'tags': tags
        }


Song.createTable(ifNotExists=True)
