##
##!/usr/bin/python 
# -*- coding: utf-8 -*-


# importeer modules
import os
import os.path                          # extract pathname en filename
import fnmatch                          # selecteer bestanden op extensie
from mutagen.mp3 import MP3             # tbv mp3s
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, UFID
from mutagen.easyid3 import EasyID3
import psycopg2                         # postgres db
import sys


DIRCOL = "/media/multimedia/multimedia/muzik3/Artiesten/Amy MacDonald/Amy MacDonald - 2007 - This Is The Life"
DIRCOL = "/media/multimedia/multimedia/muzik3"

class Mp3:
    cursor = None
    connection = None

    def __init__(self, fileMp3):
        """creatie Mp3 object
        """
        # database
        self.cursor = None
        self.connection = None
        
        # mp3 bestand
        self.fileMp3 = fileMp3

        self.length = -1
        self.bitrate = -1
        self.size = -1

        self.title = "#"
        self.album_artist = "#"
        self.artist = "#"
        self.album = "#"
        self.genre = "#"
        self.year = -1
        self.tracknumber = -1
        self.song_id = -1
        self.location = "#"
        self.filename = "#"

    def readPropertiesMp3(self):
        """readPropertiesMp3, eigenschappen bestand inlezen
        in: mp3 bestand, met volledig pad ervoor
        uit: 
        """

        ### bitrate en lengte
        self.audio = MP3(self.fileMp3)
        self.length  = int(self.audio.info.length)
        self.bitrate = int(self.audio.info.bitrate / 1000)
        self.size    = int(os.path.getsize(self.fileMp3) / 1024 / 1024)

        ### overige eigenschappen
        self.audio = EasyID3(self.fileMp3)

        # lees title
        try:
            self.title        = unicode(self.audio['title'][0])
        except KeyError:
            pass
        
        # lees album artist
        try:       
            self.album_artist = unicode(self.audio['performer'][0])
        except KeyError:
            pass

        # lees artist
        try:
            self.artist       = unicode(self.audio['artist'][0])
        except KeyError:
            pass

        # lees album
        try:
            self.album        = unicode(self.audio['album'][0])
        except KeyError:
            pass

        # lees jaar
        try:
            self.year         = int(self.audio['date'][0])
        except KeyError:
            pass

        # lees tracknumber
        try:
            self.tracknumber  = self.audio['tracknumber'][0].split('/')[0]
        except KeyError:
            pass

        # lees genre
        try:
            self.genre = unicode(self.audio['genre'][0])
        except KeyError:
            pass

        # bepaald filename
        self.filename = os.path.basename(self.fileMp3)

        # bepaal locatie
        self.location = self.fileMp3[len(DIRCOL):]
        self.location = os.path.dirname(self.location)

        ### lees UFID
        self.audio = ID3(self.fileMp3)
        if 'UFID:mc' in self.audio.keys():
            self.song_id  = self.audio.get('UFID:mc').data



    def printPropertiesMp3(self):
        """printPropertiesMp3, ingelezen eigenschappen mp3 bestand afdrukken
        """
        print "=========================================================================================="
        print 'title          : ', self.title
        print 'album artist   : ', self.album_artist
        print 'artist         : ', self.artist
        print 'album          : ', self.album
        print 'year           : ', self.year
        print 'tracknumber    : ', self.tracknumber
        print 'genre          : ', self.genre
        print "self.lenght    : ", self.length
        print "self.bitrate   : ", self.bitrate
        print "self.size      : ", self.size
        print "self.ufid      : ", self.song_id
        print "self.filename  : ", self.filename
        print "self.location  : ", self.location
        print "=========================================================================================="


    def openDB(self):
        """open connection met de database
        """
        
        ### sqlite3 open database
        # connection = sqlite3.connect(DBNAME)
        # create a cursor
        # cursor = connection.cursor()

        if Mp3.connection is None:
            ### postgresql
            try:
                Mp3.connection = psycopg2.connect(database='dbmc', user='pi', host="192.168.1.164", port="5432")
                Mp3.cursor = Mp3.connection.cursor()
                Mp3.cursor.execute('select version()')
                ver = Mp3.cursor.fetchone()
                print ver

            except psycopg2.DatabaseError, e:
                print 'Error %s' % e

        return 1

    def closeDB(self):
        """ database cursor en connectie sluiten
        """

        Mp3.cursor.close()
        Mp3.connection.close()
        

    def saveInfoMp3(self):
        """saveMp3, mp3 opslaan in de database
        """

        # controleer of al id al niet voorkomt in database, dan overslaan
        Mp3.cursor.execute("select count(*) from songs where song_id = %s" % self.song_id)
        recordset = Mp3.cursor.fetchall()
        aantal = recordset[0][0]

        if aantal == 0:
            Mp3.cursor.execute("insert into songs (title, album, artist, albumartist, year, tracknumber, genre, \
                length, bitrate, size, song_id, filename, location) \
                values('%s', '%s', '%s', '%s', %s, %s, '%s', %s, %s, %s, %s, '%s', '%s')" % \
                (q(self.title), q(self.album), q(self.artist), q(self.album_artist), self.year, \
                    self.tracknumber, q(self.genre), self.length, self.bitrate, self.size, \
                    self.song_id, q(self.filename), q(self.location)))

        # opslaan
        Mp3.connection.commit()
        # cursor.close()
        # connection.close()


def q(inString):
    """q, quotes, quotes zijn voor sqlite een probleem, die moeten ge-escaped worden
    door nog een quote"""
    uitString = ""
    for teken in inString:
        uitString = uitString + teken
        if teken == "'":
            uitString = uitString + "'"
    # print uitString
    # print type(uitString)
    if isinstance(uitString, str):
        uitString = unicode(uitString, 'utf-8', errors='replace')
    return uitString
    

if __name__ == "__main__":
    print "* * * T e s t i n g * * * "

    tel = 0
    for root, dir, files in os.walk(DIRCOL):
        print root
        for bestand in files:
            if fnmatch.fnmatch(bestand, "*.mp3"):
                tel = tel + 1
                # print str(tel) + ": " + bestand
                # object aanmaken
                song = Mp3(os.path.join(root, bestand))
                # eigenschappen inlezen
                song.readPropertiesMp3()
                if song.song_id > 0:
                    # save into database
                    # song.printPropertiesMp3()
                    song.openDB()
                    song.saveInfoMp3()
                    pass
                else:
                    print song.song_id, 'geen song_id gevonden'
    print 'Als laatste gelezen: '
    song.closeDB()
    song.printPropertiesMp3()


# eof #
