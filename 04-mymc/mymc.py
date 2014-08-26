# -*- coding: utf-8 -*-

"""Module music collection.

Doel database maken van al mijn mp3s.
Via webinterface inzicht hierin bieden, 
en afspelen via sonos.
"""

import sys
import codecs               # voor utf-8 bestanden
import os
import os.path
import datetime
from datetime import timedelta
# import sqlite3              # sqlite database
import psycopg2             # postgres db
import psycopg2.extras      # dictionary cursor
import sys
import cherrypy             # cherrypy de webinterface
import urllib               # vertaal string naar url
from soco import SoCo       # sonos

import mymc_html            # web pagina's
reload(mymc_html)
import sonos_discover	    # eigen module, haal sonos info op


# DBNAME = "../db/music_collection.db"
DBNAME = "/media/rasp163-v/mymc/db/music_collection.db"
MCSERVER = "http://192.168.1.163"
# de box die de baas is
# COORDINATOR = sonos_discover.getSonosCoordinator()
COORDINATOR = '192.168.1.21'
# locatie voor caching van bestanden
CACHE="../cache"
# cache status aan of uit
CACHING=True
# aantal dagen dat historie opgeteld moet worden
GENERATEDAYS = 100



class Mc:
    """Mc = music collection
    """

    # database connectie
    cursor = None
    connection = None
    
    def __init__(self):
        # list van historische tijdvakken, jaren, maanden, dagen
        self.periods = []

    def dbOpen(self):
        """open connection met de database
        """
        
        ### sqlite3 open database
        # connection = sqlite3.connect(DBNAME)
        # create a cursor
        # cursor = connection.cursor()

        if Mc.connection is None:
            ### postgresql
            try:
                Mc.connection = psycopg2.connect(database='dbmc', user='pi', host="mc", \
                                  port="5432")
                # gewone cursor
                # Mc.cursor = Mc.connection.cursor()
                # dictionary cursor
                Mc.cursor = Mc.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                Mc.cursor.execute('select version()')
                ver = Mc.cursor.fetchone()
                print ver

            except psycopg2.DatabaseError, e:
                print 'Error %s' % e

        return 1

    def dbClose(self):
        """ database cursor en connectie sluiten
        """

        Mc.cursor.close()
        Mc.connection.close()


    @cherrypy.expose
    def pagePlayedHistory(self, year = 0, month = 0):
        """Toon per jaar, maand en dag, aantal afgespeelde songs.
        """

        # cijfers opnieuw opbouwen, moet waarschijnlijk anders
        self.generate_periods()
        self.fill_periods()

        if year == 0 or month == 0:
            today = datetime.datetime.now()
            year = today.year
            month = today.month

        ### haal jaar, maand, en dag gegevens op, en maak er dictionaries van voor weergave op webpagina
        # haal jaren op
        query = """select year, played from played_history where month = 0"""
        records = self.dbGetData(query)
        yearsdict = {}
        for record in records:
            key = 'year' + str(record['year'])
            yearsdict[key] = record['played']
        #print records
        print 'yearsdict', yearsdict

        # haal maanden op
        query = """select year, month, played from played_history
            where year = %s and month <> 0 and day = 0""" % (year)
        
        records = self.dbGetData(query)
        monthsdict = {}
        for record in records:
            key = 'month' + str(record['month'])
            monthsdict[key] = record['played']
        print 'monthsdict', monthsdict

        # haal dagen op
        query = """select year, month, day, played from played_history
            where year = %s and month = %s and day <> 0""" % (year, month)
        records = self.dbGetData(query)
        # print query
        # print records
        daysdict = {}
        for record in records:
            key = 'day' + str(record['day'])
            daysdict[key] = record['played']
        print 'daysdict', daysdict

        h = mymc_html.pagePlayedHistory(yearsdict, monthsdict, daysdict)
        print h

        return h
    

    def fill_periods(self):

        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        query = "delete from played_history"
        self.dbOpen()
        Mc.cursor.execute(query)
        Mc.connection.commit()

        for period in self.periods:
            if period[1] == 0 and period[2] == 0:     # een jaar
                selectie = str(period[0]) + '%'
            else:
                if period[2] == 0:                   # een maand
                    selectie = str(period[0]) + '-' + str(period[1]).zfill(2) + '%'
                else:
                    selectie = selectie = str(period[0]) + '-' + str(period[1]).zfill(2) + \
                               '-' + str(period[2]).zfill(2) + '%'
            # print selectie

            query = """
                insert into played_history (year, month, day, played) 
                select %(year)s as year, %(month)s as month, %(day)s as day, count(*)
                from played
                where to_char(playdate, 'yyyy-mm-dd') like %(selectie)s
                group by year, month, day
                having count(*) <> 0
                """ % {'year': period[0], 'month': period[1], 'day': period[2], 'selectie': "'" + selectie + "'"}
            # (period[0], period[1], period[2], 'selectie' + selectie)
            print query
            Mc.cursor.execute(query)

        Mc.connection.commit()
        # cursor.close()
        # connection.close()

        return True
        

    def generate_periods(self, by=2014, bm=8, bd=1):
        """genereer perioden, jaren, jaar-maanden, datums
        in: begin year, begin month, begin day, end year
        out: list met de periods
        nb, voor het gemak gaan we er van uit dat elke maand 31 dagen telt
        """

        days = timedelta(days = 1)
        daycounter = datetime.date(by, bm, bd)
        periods = [] 

        for tel in range(GENERATEDAYS):
            # tel is generator

            new = [daycounter.year, 0, 0]
            if new not in periods:
                periods.append(new)

            new = [daycounter.year, daycounter.month, 0]
            if new not in periods:
                periods.append(new)

            new = [daycounter.year, daycounter.month, daycounter.day]
            if new not in periods:
                periods.append(new)

            daycounter = daycounter + days

        self.periods = periods
        return periods


    def partPageSongRating(self, song_id = 0):
        """
        """

        query = """select ifnull(max(rating), 0) as rating from songsinfo where song_id = %s""" % song_id
        records = self.dbGetData(query)
        # print records
        rating = records[0]['rating']
        # print 'db rating', rating

        h = mymc_html.pagePartSongRating(song_id, rating)

        return h


    @cherrypy.expose
    def pageClearCache(self):
        """Cache bestanden verwijderen.
        """

        records = []
        
        # controleer of cache directory bestaat
        if os.path.exists(CACHE):
            for root, map, files in os.walk(CACHE):
                print map
                tel = 0
                for bestand in files:
                    tel = tel + 1
                    filename = os.path.join(root, bestand)
                    # print str(tel) + ": " + filename
                    records.append(filename)
                    os.remove(filename)
        print records

        h = mymc_html.pageClearCache(records)

        return h
                

    def storeInCache(self, page="#", pagename="#", key1="#"):
        """Web pagina voor her gebruik opslaan op schijf.
        """

        if page == "#" or pagename == "#":
            return False

        if key1 <> "#":
            pagename = pagename + "_" + key1
        hfile = os.path.join(CACHE, pagename)

        # werkte niet my postgres: hhandler = codecs.open(hfile, "w", "utf-8")
        hhandler = codecs.open(hfile, "w", 'utf-8')
        # page = page.decode('utf-8', errors='replace')
        hhandler.write(page)
        hhandler.close()

        return True


    def getFromCache(self, pagename="#", key1="#", key2="#", key3="#"):
        """Check of webpagina bestaat in cache, zo ja, ophalen.
        """

        # als caching uitstaat, gebruik dan cache bestanden niet
        if not CACHING:
            return "#"

        # als geen pagina naam bekend, stop
        if pagename == "#":
            return h

        h = "#"

        if key1 <> "#":
            pagename = pagename + "_" + key1
        hfile = os.path.join(CACHE, pagename)

        if os.path.exists(hfile):
            hhandler = codecs.open(hfile, "r", "utf-8")
            page = hhandler.read()
            hhandler.close()
        else:
            page = "#"
            
        return page
    

    @cherrypy.expose
    def pageSearchResult(self, **kwargs):
        """Geef zoek resultaat terug, zoekopdracht door pageSearch.

        TODO: zoeken op rating
        TODO: zoeken op niet afgespeeld laatste #N
        """

        where = ""
        having = ""
        # print kwargs
        if 'salbumartist' in kwargs.keys():
            stitle = kwargs['salbumartist'].upper()
            if stitle <> '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.albumartist) like '%" + stitle + "%' "

        if 'sartist' in kwargs.keys():
            sartist = kwargs['sartist'].upper()
            if sartist <> '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.artist) like '" + sartist + "' "

        if 'salbum' in kwargs.keys():
            salbum = kwargs['salbum'].upper()
            if salbum <> '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.album) like '%" + salbum + "%' "

        if 'stitle' in kwargs.keys():
            stitle = kwargs['stitle'].upper()
            if stitle <> '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.title) like '%" + stitle + "%' "

        if 'syear' in kwargs.keys():
            syear = kwargs['syear'].upper()
            if syear <> '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "songs.year = " + syear + " "
                
        if 'snumplayed' in kwargs.keys():
            snumplayed = kwargs['snumplayed']
            if snumplayed <> '':
                if len(having) > 0:
                    having = having + " and "
                having = having + " count(played.song_id) < " + snumplayed

        ### filter opbouwen voor rating
        whererating = ""
        if 'srating0' in kwargs.keys():
            srating0 = kwargs['srating0']
            if srating0 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating0

        if 'srating1' in kwargs.keys():
            srating1 = kwargs['srating1']
            if srating1 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating1

        if 'srating2' in kwargs.keys():
            srating2 = kwargs['srating2']
            if srating2 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating2

        if 'srating3' in kwargs.keys():
            srating3 = kwargs['srating3']
            if srating3 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating3

        if 'srating4' in kwargs.keys():
            srating4 = kwargs['srating4']
            if srating4 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating4

        if 'srating5' in kwargs.keys():
            srating5 = kwargs['srating5']
            if srating5 <> '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " songsinfo.rating = " + srating5

        ## where rating samen voegen met andere where's
        if len(whererating) > 0:
            if len(where) > 0:
                where = where + " and "
            where = where + '(' + whererating + ')'

        ## zoeken op periode
        if 'speriod' in kwargs.keys():
            speriod = kwargs['speriod']
            # zoek uit welke periode
            if speriod == 'week':
                dagen = timedelta(days=7)
            if speriod == '4 weken':
                dagen = timedelta(days= (4*7))
            if speriod == '8 weken':
                dagen = timedelta(days= (8*7))
            if speriod == '12 weken':
                dagen = timedelta(days= (12*7))
            if speriod == 'halfjaar':
                dagen = timedelta(days= (26*7))
            if speriod == 'jaar':
                dagen = timedelta(days= (52*7))

            ouderdan = datetime.date.today() - dagen
            ouderdan = ouderdan.isoformat()
            if len(where) > 0:
                where = where + ' and '
            where = where + " played.playdate < '%s' " % ouderdan
            
        
        if len(where) > 0:
            where = "where " + where

        # print 'where : ', where
        # print 'having: ', having

        query1 = """
            select songs.song_id, songs.title, songs.album, songs.artist, songs.albumartist, songs.year
                , songs.tracknumber
                , substr(min(to_char(playdate, 'yyyy-mm-dd')), 1, 10) as first
                , substr(max(to_char(playdate, 'yyyy-mm-dd')), 1, 10) as last
                , count(played.song_id) as played
            from songs 
            left join songsinfo
            on songs.song_id = songsinfo.song_id
            left join played
            on songs.song_id = played.song_id
            """
        query2 = """
            group by songs.song_id, songs.title, songs.album, songs.artist, songs.albumartist, songs.year """
        if len(having) > 0:
            having = ' having ' + having
        query3 = " order by songs.year, songs.tracknumber limit 40 "
        query = query1 + where + query2 + having + query3
        print 'query', query

        records = self.dbGetData(query)
        # print 'records', records

        h = mymc_html.pageSearchResult(records)

        return h


    @cherrypy.expose
    def pageSearch(self):

        h = mymc_html.pageSearch()

        return h
    

    @cherrypy.expose
    def sonosSetVolume(self, speaker = COORDINATOR, volume = 10):
        """sonosSetVolume, volume voor speaker instellen
        """

        volume = int(volume)
        # verbinding maken
        sonos = SoCo(speaker)
        if volume <= 70:
            sonos.volume = volume

        # pagina laden voor als antwoord terug aan de server
        record = {'speaker': speaker, 'volume': volume}
        h = mymc_html.sonosSetVolume(record)
                
        return h


    @cherrypy.expose
    def pageSonosSpeakers(self):
        """pageSonosSpeakers, toon status sonos speaker, verander volume
        """

        # haal info voor deze pagina op
        records = sonos_discover.getSonos()

        # maak web pagina
        h = mymc_html.pageSonosSpeakers(records)

        return h
        
    
    @cherrypy.expose
    def pageInfoMc(self):
        """pageInfoMc, statistieken berekenen over de muziekcollectie 
        """

        ## info over tabel songs
        query1 = """
        select 	count(distinct albumartist) as num_albumartist
        ,       count(distinct albumartist || '#' || album) as num_album
        ,       count(distinct artist) as num_artist
        ,       count(*) as num_song
        from songs
        """
        record1 = self.dbGetData(query1)
        # print "1: ", record1

        ## info over tabel played
        query2 = """
        select count(*) as num_played from played
        """
        record2 = self.dbGetData(query2)
        # print "2: ", record2

        ## info over hoeveel songs een rating hebben
        query3 = """
        select count(*) as num_songsinfo from songsinfo
        """
        record3 = self.dbGetData(query3)

        ## info over hoeveel songs in de queue zitten
        query4 = """
        select count(*) as num_queue from queue
        """
        record4 = self.dbGetData(query4)

        # één dictionary van maken
        record = dict(record1[0].items() + record2[0].items() + record3[0].items() + \
                      record4[0].items())
        print "record ", record

        h = mymc_html.pageInfoMc
        h = (h % record)
        #print '4', h

        return h
        

    @cherrypy.expose
    def pageListAlbums_AlbumArtist(self, albumartist="XQX"):
        """ageListAlbumArtists, alle album artiesten uitlijsten
        """

        # check of pagina in de cache bestaat
        pagename = "pageListAlbums_AlbumArtist"
        h = self.getFromCache(pagename, albumartist)
        if len(h) > 1:
            return h

        #albumartist='ABBA'
        albumartist = q(albumartist)    # q(), voor namen als: Guys 'n' Dolls
        query = ("""
            select albumartist, album, year, location
            from songs
            where album || '#' || tracknumber in
            (
                select album || '#' || min(tracknumber)
                from songs 
                where upper(albumartist) = upper('%s')
                group by album 
            )
            order by year, album
        """ % albumartist)
        # print query
        
        hrecords = self.dbGetData(query)
        # print hrecords

        # haal template op en vul deze met gegevens
        h = mymc_html.pageListAlbums_AlbumArtist(hrecords)

        # sla pagina in cache op
        self.storeInCache(h, pagename = pagename, key1 = albumartist)

        return h


    def createLinkFolderJpg(self, location = ""):
        """createLinkFolderJpg, link maken naar folder.jpg bestand
        """
        if location <> "":
            folder_jpg = "/muzik3" + location + "/" + 'folder.jpg'
            folder_jpg = urllib.quote(folder_jpg)
            folder_jpg = MCSERVER + folder_jpg
        else:
            folder_jpg = ""
        return folder_jpg


    def dbGetData(self, query="select * from songs limit 5 "):
        """dbGetData, input query uitvoeren, en data terug leveren
            input: een query
            output: de data in de vorm: list, genest meerdere dictionries
        """

        # data ophalen
        # print 'query', query # zet aan voor debuggen
        self.dbOpen()

        Mc.cursor.execute(query)
        recordset = Mc.cursor.fetchall()
        print recordset

        hrecords = []
        tel = 0
        for record in recordset:
            hrecord = {}
            tel = tel + 1
            for sleutel in record.keys():
                hrecord[sleutel] = record[sleutel]
                if sleutel == "location":
                    hrecord['folder_jpg'] = self.createLinkFolderJpg(hrecord['location'])
                # aparte kolom album_link, voor bijzondere tekens in album naam zoals: #
                if sleutel == "album":
                    hrecord['album_link'] = urllib.quote(hrecord['album'].encode('utf-8'))
                if sleutel == "albumartist":
                    hrecord['albumartist_link'] = urllib.quote(hrecord['albumartist'])
                if sleutel == "title":
                    title_link = hrecord['title']
                    # title_link = unicode(title_link, 'utf-8', errors='replace')
                    print 'title_link', title_link
                    hrecord['title_link'] = urllib.quote(title_link)
            hrecord['volgnr'] = tel
            hrecords.append(hrecord)
        # print hrecords # zet aan voor debuggen 

        return hrecords


    @cherrypy.expose
    def pageListAlbumArtists(self):
        """ageListAlbumArtists, alle album artiesten uitlijsten
        """

        # gebruik pagina uit cache, als die bestaat
        pagename = "pageListAlbumArtists"
        h = self.getFromCache(pagename)
        if len(h) > 1:
            return h

        # voor postgres, over (order . . ) toegevoegd
        query = """
            select row_number() over (order by albumartist) as volgnr, albumartist, num_songs, num_albums
            from (
                select albumartist, count(*) as num_songs, count(distinct album) as num_albums
                from   songs 
                group by albumartist
                order by 1 ) as songs
        """
        hrecords = self.dbGetData(query)

        h = mymc_html.pageListAlbumArtists(hrecords)
        # saveHTMLToFile('pageListAlbumArtists', h)

        # sla pagina in cache op
        h = unicode(h, 'utf-8', errors='replace')
        self.storeInCache(h, pagename = pagename)
        
        return h

    @cherrypy.expose
    def pageSongSave(self, song_id = -1, rating = -1):
        """pageSongSave, pageSong submit verwerken en opslaan
        """
        # song_id = 255
        # rating = 4
        
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()
        self.dbOpen()
        Mc.cursor.execute("""
            select count(*) as aantal from songsinfo where song_id = %s
            """ % song_id)
        recordset = Mc.cursor.fetchall()
        recordset = recordset[0]

        if recordset['aantal'] > 0:
            # doe een update
            Mc.cursor.execute("""
                update songsinfo set rating = %s where song_id = %s
                """ % (rating, song_id))
        else:
            # doe een insert
            Mc.cursor.execute("""
                insert into songsinfo (rating, song_id) values(%s, %s)
                """ % (rating, song_id))

        Mc.connection.commit()
        # cursor.close()
        # connection.close()

        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.pageSongSave
        return h




    @cherrypy.expose
    def pageSong(self, song_id = 0):

        # song_id = 1 # alleen waarde geven als debuggen

        ### gegevens ophalen om te tonen in web pagina
        # song
        song = self.dbGetSong(song_id)

        # afspeel info
        song_playinfo = self.dbGetPlayInfoSong(song_id)
        if len(song_playinfo.keys()) < 1:
            song_playinfo['first'] = "Never"
            song_playinfo['last'] = "Never"
            song_playinfo['timesplayed'] = "0"
        # print 'song_playinfo', song_playinfo

        # rating, etc info
        song_info = self.dbGetInfoSong(song_id)
        if len(song_info.keys()) < 1:
            song_info['rating'] = 0
            song_info['notes'] = ""
        # print 'song_info', song_info

        # tel alle dict bij elkaar op
        a = dict(song.items() + song_playinfo.items() + song_info.items())
        # print 'a', a
       
        ### template voor pagina
        h = mymc_html.pageSong()
        # print 'h', h

        # items voor pagina samenstellen
        h = (h % a)
        
        return h


    def dbGetInfoSong(self, song_id = 0):
        """dbGetInfoSong, get a song record from the database with 1 song
        """

        ## controleer song_id
        if song_id < 1:
            return []
        
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        # zoek de song op in de database
        self.dbOpen()
        Mc.cursor.execute("""
            select *
            from songsinfo
            where song_id = %s
            """ % int(song_id))
        recordset = Mc.cursor.fetchall()
        print 'recordset', recordset
        
        record = {}
        if len(recordset) > 0:
            recordset = recordset[0]

            columns = recordset.keys()
            for column in columns:
                record[column] = recordset[column] 

        return record


    def dbGetPlayInfoSong(self, song_id = 0):
        """dbGetPlayInfoSong, haal afspeel gegevens over een song op:
        eerste en laatste keer, en aantal keer
        """

        ## controleer song_id
        if song_id < 1:
            return []

        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        # haal gegevens op
        self.dbOpen()
        Mc.cursor.execute("""
            select min(playdate) as first, max(playdate) as last, count(*) as timesplayed
            from played
            where song_id = %s
            group by song_id
            """ % int(song_id))
        recordset = Mc.cursor.fetchall()

        record = {}
        if len(recordset) > 0:
            recordset = recordset[0]

            columns = recordset.keys()
            for column in columns:
                record[column] = recordset[column] 

        return record


    def dbGetSong(self, song_id = 0):
        """dbGetSong, get a song record from the database with 1 song
        """

        ## controleer song_id
        if song_id < 1:
            return []
        
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        # zoek de song op in de database
        self.dbOpen()
        Mc.cursor.execute("""
            select *
            from songs
            where song_id = %s
            """ % int(song_id))
        recordset = Mc.cursor.fetchall()

        record = {}
        if len(recordset) > 0:
            recordset = recordset[0]

            columns = recordset.keys()
            for column in columns:
                record[column] = recordset[column] 

            folder_jpg = "/muzik3" + record['location'] + "/" + 'folder.jpg'
            folder_jpg = urllib.quote(folder_jpg)
            folder_jpg = MCSERVER + folder_jpg
            record['folder_jpg'] = folder_jpg

        return record


    @cherrypy.expose
    def sonos_next(self):
        """Afspeellijst <Next> button, gaat naar volgende nummer in afspeellijst.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_next()
                
        ## 
        sonos = SoCo(COORDINATOR)
        sonos.next()

        return h


    @cherrypy.expose
    def sonos_previous(self):
        """Afspeellijst, <Previous> button, gaat naar vorige nummer, in de afspeellijst.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_previous()
                
        ## 
        sonos = SoCo(COORDINATOR)
        sonos.previous()

        return h


    @cherrypy.expose
    def sonos_play(self):
        """Afspeellijst, <play> button, afspelen of doorgaan na een pauze.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_play()
                
        ## sonos, afspelen
        sonos = SoCo(COORDINATOR)
        sonos.play()

        return h


    @cherrypy.expose
    def sonos_pause(self):
        """Afspeellijst, <pause> button, afspelen pauzeren.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_pause()
                
        ## sonos, afspelen pauzeren
        sonos = SoCo(COORDINATOR)
        sonos.pause()

        return h


    @cherrypy.expose
    def sonos_clear_queue(self):
        """sonos_clear_queue, maak sonos afspeellijst leeg
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_clear_queue
                
        ## queue leegmaken als er wat in zit
        sonos = SoCo(COORDINATOR)
        # als de sonos queue niet leeg is
        if len(sonos.get_queue()) > 0:
            ## sonos queue leegmaken
            sonos.clear_queue()

            ## table queue leegmaken
            # connection = sqlite3.connect(DBNAME)
            # cursor = connection.cursor()

            self.dbOpen()
            query = """delete from queue"""
            Mc.cursor.execute(query)
            Mc.connection.commit()
            # cursor.close()
            # connection.close()

        return h


    @cherrypy.expose
    def sonos_play_from_queue(self):
        """sonos_play_from_queue, speelt queue af
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = mymc_html.sonos_play_from_queue

        # queue afspelen als deze niet leeg is
        sonos = SoCo(COORDINATOR)
        if len(sonos.get_queue()) > 0:
            sonos.play_from_queue(0)

        return h


    @cherrypy.expose
    def sonos_playmenu(self):
        """sonos_menu, menu om commando's aan sonos te geven en info op te halen
        """

        # haal pagina op
        h = mymc_html.sonos_playmenu()

        # verbinding maken met sonos
        sonos = SoCo(COORDINATOR)

        # wat speelt er nu, als het nummer niet uit playlist komt, is current_track niet gevuld
        current_song = sonos.get_current_track_info()
        current_track = int(current_song['playlist_position'])

        # haal queue uit database op
        query = """select * from queue order by queue_id"""
        records = self.dbGetData(query)
        print 'queue records', records

        # list songs in sonos queue
        if len(sonos.get_queue()) > 0:
            ht = """<html>
<h2>Sonos queue</h2>"""
            ht = ht + "<table> "
            ht = ht + """<tr><th class="info">Info</th> <th class="track">Track</th> <th class="title">Titel</th>  <th class="artist">Artiest</th> <th class="album">Album</th></tr>"""
            tel = 0
            for song in sonos.get_queue():
                tel = tel + 1
                ht = ht + "<tr>"

                ht = ht + '<td class="info">'
                if (tel -1) < len(records):
                    record = records[tel -1]
                    song_id = record['song_id']
                    ht = ht + '<a href="pageSong?song_id=%s">Info</a>' % song_id
                ht = ht + "</td>"
                    
                if tel == current_track:
                    ht = ht + '<td class="track">' + ">" + str(tel) + "< </td>"
                else:
                    ht = ht + '<td class="track">' + str(tel) + "</td>"

                ht = ht + '<td class="title">' + song.title + "</td>"
                # gegevens kunnen None zijn als de sonos server de gegevens nog niet heeft opgehaald
                if song.creator is None:
                    ht = ht + '<td class="artist">' + "</td>"
                else:
                    ht = ht + '<td class="artist">' + song.creator + "</td>"
                    
                if song.album is None:
                    ht = ht + '<td class="album">' + "</td>"
                else:
                    ht = ht + '<td class="album">' + song.album + "</td>"

                ht = ht + "<td>"
                # rating invoeren
                # ht = ht + self.partPageSongRating(song_id)
                ht = ht + "</td> "
                ht = ht + "</tr>"
            ht = ht + "</table>"
            h = h + ht

        return h
    

    @cherrypy.expose
    def playAlsoSong(self, song_id=0):
        """playAlsoSong, nummer toevoegen aan afspeellijst, met: add_uri_to_queue(uri)
        """
        
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        self.dbOpen()
        # zoek de song op in de database
        Mc.cursor.execute("""
            select *
            from songs
            where song_id = %s
            """ % int(song_id))
        recordset = Mc.cursor.fetchall()
        # controleren als niets gevonden
        record = recordset[0]

        # uri samenstellen van de song
        uri = "/muzik3" + record['location'] + "/" + record['filename']
        print uri
        print type (uri)

        # een pagina maken, deze geeft browser meteen opdracht terug te gaan naar vorige pagina
        h = """
        <html>
        werkt het ?</br>
        %s

        <script>
            window.history.back();
        </script>

        </html>
        """ % uri

        ## stuur nummer naar sonos
        sonos = SoCo(COORDINATOR)
        # TODO zonder encode werkte niet voor bijvoorbeeld: Nånting Är På Väg
        uri = urllib.quote(uri).encode('utf8')
        uri = MCSERVER + uri
        print uri
        sonos.add_uri_to_queue(uri)

        ## log song in database als afgespeeld
        self.dbOpen()
        query = "insert into played (song_id) values(%s)" % song_id
        Mc.cursor.execute(query)
        # cursor.close()
        # connection.close()

        # stop song_id in queue table
        query = """insert into queue (song_id) values (%s) """ % song_id
        Mc.cursor.execute(query)

        # opslaan
        Mc.connection.commit()

        return h
    
        
    @cherrypy.expose
    def playSong(self, song_id=0):
        """playSong, song naar sonos sturen om af te spelen
        """

        # verbinding maken met database
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        self.dbOpen()
        # zoek de song op in de database
        Mc.cursor.execute("""
            select *
            from songs
            where song_id = %s
            """ % int(song_id))
        recordset = Mc.cursor.fetchall()
        # controleren als niets gevonden
        record = recordset[0]

        uri = "/muzik3" + record['location'] + "/" + record['filename']
        # print uri
        # print type (uri)
        
        h = """
        <html>
        werkt het ?</br>
        %s

        <script>
            window.history.back();
        </script>

        </html>
        """ % str(uri)

        ## stuur nummer naar sonos
        sonos = SoCo(COORDINATOR)
        # sonos.play_uri(
        #  'http://192.168.1.163/muzik4/Hitzone%20CDs/Hitzone%20Jaren/Hitzone%20Best%20Of%202013/Hitzone%20Best%20Of%202013%20-%20CD1/003%20-%20Lorde%20-%20Royals.mp3')
        uri = urllib.quote(uri)
        uri = MCSERVER + uri
        print uri
        sonos.play_uri(uri)

        ## log song in database als afgespeeld
        Mc.cursor.execute("insert into played (song_id) values(%s)" % song_id)
        # opslaan
        Mc.connection.commit()
        # cursor.close()
        # connection.close()

        # verstuur pagina naar de server
        return h


    @cherrypy.expose
    def listAlbumTracks(self, album="nothing"):

        pagename = "listAlbumTracks"

        h = self.getFromCache(pagename, album)
        if len(h) > 1:
            return h
        
        # connection = sqlite3.connect(DBNAME)
        # connection.row_factory = sqlite3.Row
        # cursor = connection.cursor()

        # album = "This Is The Life"
        # print 'album', album
        self.dbOpen()
        Mc.cursor.execute("""
            select *
            from songs
            where album = '%s'
            order by tracknumber
            """ % q(album))
        recordset = Mc.cursor.fetchall()

        h = "".encode('utf-8')
        h = """
        <html>
        <head>
        <title>albums</title>
        </head>
        <body>
        """ + mymc_html.main_navigation() + """
        <h1>album: %s</h1>
        <table>
        <tr><th>Playlist</th><th>Play</th><th>Track</th><th>Titel</th><th>Lengte</th><th>Bitrate</th>
        """ % album

        for song in recordset:
            print str(song['tracknumber']), song['title']
            print 'h', type(h)
            h = h + "<tr>"
            h = h + "<td>" + '<a href="playAlsoSong?song_id=' + str(song['song_id']) + '">'
            h = h + " Add " + "</a>" + "</td>"
            h = h + "<td>" + '<a href="playSong?song_id=' + str(song['song_id']) + '">'
            h = h + " Play " + "</a>" + "</td>"
            h = h + "<td>" + str(song['tracknumber']) + "</td>"
            title = song['title']
            title = unicode(title, 'utf-8', errors='replace')
            print 'title', type(title), title
            h = h + "<td>" + title + "</a>" + "</td>"
            h = h + "<td>" + str(song['length']) + "</td>"
            h = h + "<td>" + str(song['bitrate']) + "</td>"
            h = h + "<td>" + '<a href="pageSong?song_id=' + str(song['song_id']) + '">'
            h = h + "Infopage" + '</a>' + "</td>" + \
            "</tr>"

        h = h + """
        </table>
        <p></p>
        </body>
        </html>
        """

        self.storeInCache(h, pagename = pagename, key1 = album)

        return h


    @cherrypy.expose
    def index(self):
        """Start pagina van mc, alleen maar een menu.
        """
        
        return mymc_html.pageIndex()
        
        
    @cherrypy.expose
    def index_oud(self):
        # connectie met db en records ophalen
        connection = sqlite3.connect(DBNAME)
        cursor = connection.cursor()

        cursor.execute("""
            select album, year, albumartist, count(*) as aantal
            from songs
            group by albumartist, year, album
            order by albumartist, year, album
            """)
        recordset = cursor.fetchall()

        h = """
        <html>
        <a href="sonos_menu">Sonos</a>
        <a href="pageListAlbumArtists">Album artiesten</a>
        <a href="pageInfoMc">Info Mc</a>
        <head>
        <title>albums</title>
        </head>
        <body>
        <h1>Albums in mijn collectie</h1>
        <table>
        <tr><th>Artiest</th><th>Album</th><th>Nummers</th><th>Jaar</th></tr>
        """

        for album in recordset:
            # print album[0]
            h = h + "<tr><td>" + album[2] + "</td>" + \
                "<td>" + album[0] + "</td>" + \
                '<td>' + str(album[3]) + '</td>' + \
                '<td><a href="listAlbumTracks?album=' + urllib.quote(album[0]) + '">' + \
                    str(album[1]) + "</td>" + \
                "</tr>" + \
                "</a>"

        h = h + """
        </table>
        </body>
        </html>
        """

        return h


def saveHTMLToFile(filename, page):
    """HTML opslaan als een bestand, tbv debugging
    """

    # page = unicode(page, 'utf-8', errors='replace')
    filename = filename + "-debug.html"
    f = codecs.open(filename, 'w', "utf-8")
    f.write(page)
    f.close()

    return page

def q(inString):
    """functie: q, quotes, quotes zijn voor sqlite een probleem, die moeten ge-escaped worden
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


if __name__ == '__main__' and not 'idlelib.__main__' in sys.modules:
    conf = {
         '/': {
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': '../public'
         }
     }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
	                    'server.socket_port': 8081,
    })
    cherrypy.quickstart(Mc(), '/', conf)



