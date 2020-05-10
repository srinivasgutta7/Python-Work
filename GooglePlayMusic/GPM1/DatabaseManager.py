import sqlite3
from gmusicapi import Mobileclient

class GPMDBManager:

    def __init__(self):
        self.dbName = "GPM.db"

        # Table Songs
        self.tableSongs = "Songs"

        # Column for Table Songs
        self.colSongName = "songName"
        self.colSongAlbum = "songAlbum"
        self.colSongArtist = "songArtist"
        self.colSongDurationMillis = "songDurationMillis"
        self.colSongPlayCount = "songPlayCount"
        self.colSongRating = "songRating"
        self.colSongComposer = "songComposer"
        self.colSongYear = "songYear"

        __CREATE_TABLE_SONGS = """CREATE TABLE IF NOT EXISTS Songs (songName TEXT, songAlbum TEXT,
                                    songArtist TEXT, songDurationMillis INTEGER, songPlayCount INTEGER,
                                    songRating TEXT, songComposer TEXT, songYear INTEGER)"""

        self.conn = None

        self.connect()
        c = self.conn.cursor()
        c.execute(__CREATE_TABLE_SONGS)

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbName)
            #self.conn.text_factory = lambda x: str(x, "utf-16")

    def insertSong(self, songName, songAlbum, songArtist, songDuration, songCount, songRating, songComposer, songYear):
        INSERT_SONG = """INSERT INTO Songs VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

        c = self.conn.cursor()
        c.execute(INSERT_SONG, (songName, songAlbum, songArtist, songDuration, songCount, songRating, songComposer, songYear))
        self.conn.commit()

    def selectSongByName(self, songName):
        SELECT_BY_NAME = """SELECT * FROM Songs WHERE (songName=?) LIMIT 1"""

        c = self.conn.cursor()
        return c.execute(SELECT_BY_NAME, (songName,)).fetchone()

    def selectSongOrderByPlayCount(self, limit=None):
        if limit is None:
            SELECT_ORDER_PLAY_COUNT = """SELECT * FROM Songs ORDER BY songPlayCount DESC"""
        else:
            SELECT_ORDER_PLAY_COUNT = "SELECT * FROM Songs ORDER BY songPlayCount DESC LIMIT " + str(limit)

        c = self.conn.cursor()
        return c.execute(SELECT_ORDER_PLAY_COUNT)

    def selectSongsHeardBefore(self):
        SELECT = """SELECT * FROM Songs WHERE (songPlayCount > 0) ORDER BY songPlayCount DESC"""
        c = self.conn.cursor()
        return c.execute(SELECT)

    def deleteAllSongs(self):
        TRUNCATE_SONGS = """DELETE FROM Songs"""
        self.conn.cursor().execute(TRUNCATE_SONGS)

    def close(self):
        self.conn.close()
        self.conn = None

if __name__ == "__main__":
    manager = GPMDBManager()

    """
    Load all songs into db (Use ONLY ONCE)
    """

    ANDROID_DEVICE_MAC_ADDRESS = "00:00:00:00:00:00"

    client = Mobileclient()
    client.login("abc@gmail.com", "xyz", ANDROID_DEVICE_MAC_ADDRESS)

    print("Getting songs")

    library = client.get_all_songs()
    print("Retreived all songs")

    for i, songDict in enumerate(library):
        name = songDict["title"]
        album = songDict["album"]
        artist = songDict["artist"]
        duration = songDict["durationMillis"]
        playCount = songDict["playCount"]
        songRating = songDict["rating"]
        songComposer = songDict["composer"]
        songYear = songDict["year"]

        manager.insertSong(name, album, artist, duration, playCount, songRating, songComposer, songYear)
        print("Inserted Song %d : Name = %s" % ((i+1), name))


    manager.close()
