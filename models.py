import os
import json
from sqlobject import SQLObject, sqlhub, connectionForURI, StringCol, BigIntCol, BoolCol

db_filename = os.path.abspath('data.db')
connection_string = 'sqlite:' + db_filename
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
    liked = BoolCol()

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
            'tags': tags,
            'liked': self.liked
        }


Song.createTable(ifNotExists=True)
