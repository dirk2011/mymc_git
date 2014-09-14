# -*- coding: utf-8 -*-

"""Module met database functies.

Voor opvragen gegevens, en wijzigingen uitvoeren.
Tevens functies voor specifieke taken.
"""


__author__  = 'dp'
__date__    = '2014-09-14'


# imports
import psycopg2             # postgres db
import psycopg2.extras      # dictionary cursor
import urllib               # vertaal string naar url
import codecs               # voor utf-8 bestanden

# dbconnectie
DBNAME="dbmc"
DBUSER="pi" 
DBHOST="mc"
DBPORT="5432"


class MyDB():
    _db_connection = None
    _db_cur = None
    
    def __init__(self):
        ### postgresql
        try:
            self._db_connection = psycopg2.connect(database=DBNAME, user=DBUSER, host=DBHOST, port=DBPORT)
            # gewone cursor
            # Mc.cursor = Mc.connection.cursor()
            # dictionary cursor
            self._db_cur = self._db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self._db_cur.execute('select version()')
            ver = self._db_cur.fetchone()
            print ver

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e


    def __del__(self):
        self._db_connection.close()


    def dbGetData(self, query="select * from songs limit 5 "):
        """dbGetData, Voer een query uit en geef data terug..
        @param query: de uit te voeren query.
        @return: de data in de vorm: list, genest meerdere dictionries
        """

        self._db_cur.execute(query)
        recordset = self._db_cur.fetchall()
        # print recordset

        hrecords = []
        tel = 0
        for record in recordset:
            hrecord = {}
            tel = tel + 1
            for sleutel in record.keys():
                hrecord[sleutel] = record[sleutel]
                if sleutel == u"location":
                    pass
                    # hrecord[u'folder_jpg'] = self.createLinkFolderJpg(hrecord[u'location'])
                # aparte kolom album_link, voor bijzondere tekens in album naam zoals: #
                if sleutel == u"album" and hrecord[u'album'] is not None:
                    hrecord[u'album_link'] = urllib.quote(hrecord[u'album'].encode('utf-8'))
                if sleutel == u"albumartist":
                    hrecord[u'albumartist_link'] = urllib.quote(hrecord[u'albumartist'])
                    hrecord[u"albumartist"] = hrecord[u"albumartist"].decode('utf-8', errors='replace') 
                if sleutel == u"title" and hrecord[u'title'] is not None:
                    title_link = hrecord[u'title']
                    hrecord[u'title_link'] = urllib.quote(title_link)
                    hrecord[u"title"] = hrecord[u"title"].decode('utf-8', errors='replace')
                    # print 'title_link', title_link
                if sleutel == u"artist" and hrecord[u'artist'] is not None:
                    hrecord[u"artist"] = hrecord[u"artist"].decode('utf-8', errors='replace')
            hrecord[u'volgnr'] = tel
            hrecords.append(hrecord)
        # print hrecords # zet aan voor debuggen

        return hrecords


    def dbExecute(self, query):
        """Voer queries uit, niet om gegevens op te halen, maar data manipulatie,
        zoals inserts, deletes, etc"""

        self._db_cur.execute(query)
        # print 'query', query
        self._db_connection.commit()


def dbGetSongInfoPlayed(song_id="0"):
    """Haal afspeel gegevens over een song op: eerste en laatste keer, en aantal keer
    """

    # haal gegevens op
    query = """
        select   to_char(min(playdate), 'yyyy-mm-dd hh24:mi') as first
        ,        to_char(max(playdate), 'yyyy-mm-dd hh24:mi') as last
        ,        count(*) as timesplayed
        from     played
        where    song_id = %s
        """ % int(song_id)

    db = MyDB()
    records = db.dbGetData(query)
    print 'dbGetPlayInfoSong - records', records
    print 'query: ', query

    if len(records) == 1:
        record = records[0]
    else:
        record = {}

    return record


def dbSongsUpdateAlbumId():
    """Update table songs, vul album_id als deze nog leeg is, zoek op in table albums.
    """

    # database connection maken
    db = MyDB()

    # zoek alle songs waarvan album_id leeg is
    query = """select song_id, albumartist, album, album_id
        from songs
        where album_id is null order by song_id"""
    songs = db.dbGetData(query)
    print 'lengte songs: ', len(songs)

    tel = 0
    # doorloop alle songs met lege album_id
    for song in songs:
        # zoek album op in table albums
        query = """select * from albums
            where upper(albumartist) = upper('%s')
              and upper(album) = upper('%s')""" % (q(song['albumartist']), q(song['album']))
        album = db.dbGetData(query)
        if len(album) == 0:
            # als niet gevonden voeg album toe
            query = """insert into albums (albumartist, album)
                values ('%s', '%s') """ % (q(song['albumartist']), q(song['album']))
            db.dbExecute(query)
            # zoek toegevoegde record op voor de id
            query = """select * from albums
                where upper(albumartist) = upper('%s')
                  and upper(album) = upper('%s')""" % (q(song['albumartist']), q(song['album']))
            album = db.dbGetData(query)

        if len(album) > 0:
            # update songs, vul album_id
            album = album[0]
            print tel, "song: ", song['album'], " album: ", album['album']
            query = """update songs
                set album_id = %s
                where song_id = %s """ % (album['album_id'], song['song_id'])
            db.dbExecute(query)

        # beperk het bijwerken tot een maximum                
        tel = tel + 1
        if tel > 3000:
            break
        
    return tel


def dbSongsUpdateAlbumArtistId():
    """Update table songs, vul albumartist_id als deze nog leeg is, zoek op in table albumartists.
    """
    
    # database connection
    db = MyDB()

    # zoek alle songs waarvan artist_id leeg is
    query = """select song_id, albumartist, albumartist_id
        from songs
        where albumartist_id is null order by song_id"""
    songs = db.dbGetData(query)
    print 'lengte songs: ', len(songs)

    tel = 0
    # doorloop alle songs met lege albumartist_id
    for song in songs:
        # zoek albumartist op in table albumartists
        query = """select * from albumartists
            where upper(albumartist) = upper('%s') """ % q(song['albumartist'])
        albumartist = dbGetData(query)
        if len(albumartist) == 0:
            # als niet gevonden voeg artist toe
            query = """insert into albumartists (albumartist)
                values ('%s') """ % q(song['albumartist'])
            db.dbExecute(query)
            # zoek toegevoegde record op voor de id
            query = """select * from albumartists
                where upper(albumartist) = upper('%s') """ % q(song['albumartist'])
            albumartist = db.dbGetData(query)

        if len(albumartist) > 0:
            # update songs, vul albumartist_id
            albumartist = albumartist[0]
            print tel, "song: ", song['albumartist'], " albumartists: ", albumartist['albumartist']
            query = """update songs
                set albumartist_id = %s
                where song_id = %s """ % (albumartist['albumartist_id'], song['song_id'])
            db.dbExecute(query)

        # beperk het bijwerken tot een maximum                
        tel = tel + 1
        if tel > 3000:
            break
    
    return tel


def dbSongsUpdateArtistId():
    """Update table songs, vul artist_id als deze nog leeg is, zoek op in table artists.
    """

    # zoek alle songs waarvan artist_id leeg is
    query = """select song_id, artist, artist_id, artist from songs where artist_id is null order by song_id"""
    songs = db.dbGetData(query)
    print 'lengte songs: ', len(songs)

    tel = 0
    # doorloop alle songs met lege artist_id
    for song in songs:
        # zoek artist op in table artists
        query = """select * from artists where upper(artist) = upper('%s') """ % q(song['artist'])
        artist = db.dbGetData(query)
        if len(artist) == 0:
            # als niet gevonden voeg artist toe
            query = "insert into artists (artist) values ('%s') " % q(song['artist'])
            db.dbExecute(query)
            # zoek toegevoegde record op voor de id
            query = """select * from artists where upper(artist) = upper('%s') """ % q(song['artist'])
            artist = db.dbGetData(query)

        if len(artist) > 0:
            # update songs, vul artist_id
            artist = artist[0]
            print tel, "song: ", song['artist'], " artists: ", artist['artist']
            query = """update songs
                set artist_id = %s
                where song_id = %s """ % (artist['artist_id'], song['song_id'])
            db.dbExecute(query)

        # beperk het bijwerken tot een maximum                
        tel = tel + 1
        if tel > 3000:
            break
        
    return tel
