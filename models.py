import os
import json
from sqlobject import SQLObject, sqlhub, connectionForURI, StringCol, BigIntCol

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'art': self.art,
            'added': self.added,
            'url': self.url,
            'tags': json.loads(self.tags)
        }


Song.createTable(ifNotExists=True)
