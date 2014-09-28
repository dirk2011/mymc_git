# -*- coding: utf-8 -*-

"""Module music collection.

Doel database maken van al mijn mp3s.
Via webinterface inzicht hierin bieden,
en afspelen via sonos.
"""

__author__  = 'dp'
__date__    = '2014-09'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


import sys
import codecs               # voor utf-8 bestanden
import os
import os.path
import datetime
from datetime import timedelta
import psycopg2             # postgres db
import psycopg2.extras      # dictionary cursor
import cherrypy             # cherrypy de webinterface
import urllib               # vertaal string naar url
import soco                 # sonos
from soco import SoCo

import mymc_html            # web pagina's
reload(mymc_html)
import sonos_discover	    # eigen module, haal sonos info op

from htable import hTable
from hTable import Html
from hTable import hLink
from hTable import TDO, TDC, TRO, TRC, TABO, TABC

from dbfunc import dbSongsUpdateAlbumId
from dbfunc import dbSongsUpdateAlbumArtistId
from dbfunc import dbSongsUpdateArtistId
from dbfunc import MyDB
from dbfunc import dbGetSongInfoPlayed
from dbfunc import q

import queuebeheer.queuebeheer
import selections.selections           # pagina muteren selecties
import searchwithselections.searchwithselections     # pagina om met selecties te zoeken


# dbconnectie
DBNAME="dbmc"
DBUSER="pi" 
DBHOST="mc"
DBPORT="5432"

MCSERVER = "http://192.168.1.163"
# de box die de baas is
# COORDINATOR = sonos_discover.getSonosCoordinator()
COORDINATOR = '192.168.1.21'
# locatie voor caching van bestanden
CACHE = "../cache"
# cache status aan of uit
CACHING = True
# aantal dagen dat historie opgeteld moet worden
GENERATEDAYS = 100
DEBUG = True # print commando's aan of uit


class Mc:
    """Mc = music collection
    """

    # database connectie
    cursor = None
    connection = None

    def __init__(self):
        """Initialiseren Mc object.
        """
        #  database openen
        self._db = MyDB()
        
        # list van historische tijdvakken, jaren, maanden, dagen
        self.periods = []


    @cherrypy.expose
    def index(self):
        """Start pagina van mymc.
        """
        
        return mymc_html.pageIndex()


    @cherrypy.expose
    def pageMenuSearch(self):
        """Menu pagina voor zoeken.
        """

        h = mymc_html.pageMenuSearch()

        return h


    @cherrypy.expose
    def pageAfgespeeld(self):
        """Menu pagina voor afgespeeld
        """

        h = mymc_html.pageAfgespeeld()

        return h


    @cherrypy.expose
    def pageBeheer(self):
        """Menu pagina voor beheer.
        """

        h = mymc_html.pageBeheer()

        return h


    @cherrypy.expose
    def pagePlayedArtistsPeriodAlbums(self, period, artist_id):
        """Afgespeelde songs per artiest en per album.
        """

        print 'period', period
        print 'artist_id', artist_id

        query = """
            select * from played_artists
            where period = '%s' and aat = 'albums' and artist_id = %s
            order by played desc
        """ % (period, int(artist_id))
        records = self._db.dbGetData(query)
        print 'records', records

        h = mymc_html.pagePlayedArtistsPeriodAlbums(period, artist_id, records)

        return h


    @cherrypy.expose
    def pagePlayedArtistsPeriod(self, period):
        """Afgespeelde songs per artiest, 1e selectie, welke periode
        """

        query = """select * from played_artists
            where period = '%s' and aat = 'artists'
            order by played desc
            """ % period

        records = self.dbGetData(query)

        h = mymc_html.pagePlayedArtistsPeriod(period, records)

        return h


    @cherrypy.expose
    def pagePlayedArtists(self):
        """Afgespeelde songs per artiest, 1e selectie, welke periode
        """

        h = mymc_html.pagePlayedArtists()

        return h


    @cherrypy.expose
    def pageRefreshPlayedArtists(self):
        """Verversen cijfers voor played artists.
        """

        # cijfers opnieuw opbouwen, moet waarschijnlijk anders
        self.dbLoadPlayedArtists()

        h = mymc_html.pageRefreshPlayedArtists()
        # print 'pageRefreshPlayedArtists', h

        return h


    def dbLoadPlayedArtists(self):
        """Table played_artists verversen.
        """

        # het gaat om 7 tijdvakken, elk tijdvak heeft 3 totalen
        periods = {'lastday': 1, 'lastweek': 7, 'last4weeks': (4 * 7), \
                   'last3months': (13 * 7), 'lasthalfyear': (26 * 7), \
                   'lastyear': (52 * 7), 'alltime': 10000}
        levels = ['artists', 'albums', 'titles']

        query1 = """-- artiest
        insert into     played_artists (period, aat, artist, artist_id, played)
        select 		'%(period)s', '%(level)s', max(artist), artist_id, count(*) as aantal
        from   		played
        left join 	songs
        on 		    played.song_id = songs.song_id
        where		current_date - date(played.playdate) < %(days)s
        group by 	artist_id
        order by 	5 desc
        limit 		100 """

        query2 = """-- artiest, albums
        insert into     played_artists (period, aat, artist, artist_id, album, album_id, played)
        select 		'%(period)s', '%(level)s', max(artist), artist_id, max(album), album_id, count(*) as aantal
        from   		played
        left join 	songs
        on 		    played.song_id = songs.song_id
        where		current_date - date(played.playdate) < %(days)s
        group by 	artist_id, album_id
        order by 	7 desc
         """

        query3 = """-- artiest, albums, songs
        insert into     played_artists (period, aat, artist, artist_id, album, album_id, title, song_id, played)
        select 		'%(period)s', '%(level)s', max(artist), artist_id
                    , max(album), album_id, max(title), songs.song_id, count(*) as aantal
        from   		played
        left join 	songs
        on 		    played.song_id = songs.song_id
        where		current_date - date(played.playdate) < %(days)s
        group by 	artist_id, album_id, songs.song_id
        order by 	9 desc
        limit 		10 """

        # vorige cijfers verwijderen
        self.dbExecute('delete from played_artists')

        tel = 0
        # cijfers ophalen
        for period in periods:
            level = levels[0]
            self.dbExecute(query1 % {'period': period, 'days': periods[period], 'level': level})

            level = levels[1]
            self.dbExecute(query2 % {'period': period, 'days': periods[period], 'level': level})

            level = levels[2]
            self.dbExecute(query3 % {'period': period, 'days': periods[period], 'level': level})
            tel = tel + 3
            print 'teller: ', tel
            # break


    @cherrypy.expose
    def pageRefreshPlayedHistory(self):
        """Verversen cijfers voor played history.
        """

        # cijfers opnieuw opbouwen, moet waarschijnlijk anders
        self.generate_periods()
        self.fill_periods()

        # html pagina opbouwen
        h = mymc_html.pageRefreshPlayedHistory()
        # print 'pageRefreshPlayedHistory', h

        return h
        

    @cherrypy.expose
    def pagePlayedHistoryDetails(self, datum="#"):
        
        # als geen datum ontvangen, doe niets
        if datum == "#":
            return
        
        records = self.dbGetSongs(playdate=datum)
        
        h = mymc_html.pagePlayedHistoryDetails(datum, records)
        
        return h

    
    @cherrypy.expose
    def pagePlayedHistory(self, year=0, month=0):
        """Toon per jaar, maand en dag, aantal afgespeelde songs.
        """

        if year == 0 or month == 0:
            today = datetime.datetime.now()
            year = today.year
            month = today.month

        ### haal jaar, maand, en dag gegevens op, en maak er dictionaries van voor weergave op webpagina
        # haal jaren op
        db = MyDB()
        query = """select year, played from played_history where month = 0"""
        records = db.dbGetData(query)
        yearsdict = {}
        for record in records:
            key = 'year' + str(record['year'])
            yearsdict[key] = record['played']
        # voeg ook year en month toe aan dictionary
        yearsdict['year'] = year
        yearsdict['month'] = month
        #print records
        #print 'yearsdict', yearsdict

        # haal maanden op
        query = """select year, month, played from played_history
            where year = %s and month <> 0 and day = 0""" % (year)
        records = db.dbGetData(query)
        monthsdict = {}
        for record in records:
            key = 'month' + str(record['month'])
            monthsdict[key] = record['played']
        # voeg ook year en month toe aan dictionary
        monthsdict['year'] = year
        monthsdict['month'] = month
        # print 'monthsdict ->', monthsdict

        # haal dagen op
        query = """select year, month, day, played
            , ltrim(to_char(year, '9999')) || ltrim(to_char(month, '09')) || ltrim(to_char(day, '09')) as datum
            from played_history
            where year = %s and month = %s and day <> 0""" % (year, month)
        records = db.dbGetData(query)
        # print query
        # print records
        daysdict = {}           # per dagnr de afgespeelde records
        for record in records:
            key = 'day' + str(record['day'])
            key2 = 'dayb' + str(record['day'])
            daysdict[key] = record['played']
            daysdict[key2] = record['datum']
        # print 'daysdict', daysdict

        h = mymc_html.pagePlayedHistory(yearsdict, monthsdict, daysdict)
        # print h

        return h
    

    def fill_periods(self):
        """Cijfers opbouwen voor pagePlayedHistory
        """

        # oude gegevens verwijderen
        query = "delete from played_history"
        self.dbOpen()
        Mc.cursor.execute(query)
        Mc.connection.commit()

        tel = 0
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
            # print query
            tel = tel + 1
            print 'query: ', tel
            Mc.cursor.execute(query)

        Mc.connection.commit()

        return True
        

    def generate_periods(self, by=2014, bm=8, bd=1):
        """genereer perioden, jaren, jaar-maanden, datums
        in: begin year, begin month, begin day, end year
        out: list met de periods
        nb, voor het gemak gaan we er van uit dat elke maand 31 dagen telt
        """

        days = timedelta(days=1)
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


    def partPageSongRating(self, song_id=0):
        """html code om song rating in te voegen
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
            for root, map2, files in os.walk(CACHE):
                tel = 0
                for bestand in files:
                    tel = tel + 1
                    filename = os.path.join(root, bestand)
                    # print str(tel) + ": " + filename
                    records.append(filename)
                    os.remove(filename)
        # print records

        h = mymc_html.pageClearCache(records)

        return h


    @cherrypy.expose
    def pageShowCache(self):
        """Toon bestanden in cache.
        """

        records = []
        
        # controleer of cache directory bestaat
        if os.path.exists(CACHE):
            for root, map2, files in os.walk(CACHE):
                tel = 0
                for bestand in files:
                    tel = tel + 1
                    filename = os.path.join(root, bestand)
                    filename = filename.decode('utf-8', errors='replace')
                    # print str(tel) + ": " + filename
                    record = {}
                    record['volgnr'] = tel
                    record['bestand'] = filename
                    records.append(record)

        # return str(records)
        h = mymc_html.pageShowCache(records)

        return h


    def storeInCache(self, page="#", pagename="#", key1="#"):
        """Web pagina voor hergebruik opslaan op schijf.
        """

        # page = webpagina, pagename = pagina naam
        if page == "#" or pagename == "#":
            return False

        # key1 = eventueel een parameter van de pagina
        if key1 != "#":
            pagename = pagename + "_" + key1
        hfile = os.path.join(CACHE, pagename)

        # probeer pagina te vertalen naar utf-8
        try:
            page = unicode(page, 'utf-8', errors='replace')
        except TypeError:
            pass
        
        with codecs.open(hfile, "w", 'utf-8') as f:
            f.write(page)

        return True


    def getFromCache(self, pagename="#", key1="#", key2="#", key3="#"):
        """Check of webpagina bestaat in cache, zo ja, ophalen.
        """

        # als caching uitstaat, gebruik dan cache bestanden niet
        if not CACHING:
            return "#"

        h = " "

        # als geen pagina naam bekend, stop
        if pagename == "#":
            return h

        if key1 != "#":
            pagename = pagename + "_" + key1
        hfile = os.path.join(CACHE, pagename)

        if os.path.exists(hfile):
            with codecs.open(hfile, "r", "utf-8") as f:
                page = f.read()
        else:
            page = "#"
            
        return page
    

    @cherrypy.expose
    def pageSearchResult(self, **kwargs):
        """Geef zoek resultaat terug, zoekopdracht door pageSearch.
        """

        where = ""
        having = ""
        # print kwargs
        if 'salbumartist' in kwargs.keys():
            stitle = kwargs['salbumartist'].upper()
            if stitle != '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.albumartist) like '%" + stitle + "%' "

        if 'sartist' in kwargs.keys():
            sartist = kwargs['sartist'].upper()
            if sartist != '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.artist) like '" + sartist + "' "

        if 'salbum' in kwargs.keys():
            salbum = kwargs['salbum'].upper()
            if salbum != '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.album) like '%" + salbum + "%' "

        if 'stitle' in kwargs.keys():
            stitle = kwargs['stitle'].upper()
            if stitle != '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "upper(songs.title) like '%" + stitle + "%' "

        if 'syear' in kwargs.keys():
            syear = kwargs['syear'].upper()
            if syear != '':
                if len(where) > 0:
                    where = where + " and "
                where = where + "songs.year = " + syear + " "

        if 'snumplayed' in kwargs.keys():
            snumplayed = kwargs['snumplayed']
            if snumplayed != '':
                if len(having) > 0:
                    having = having + " and "
                having = having + " count(played.song_id) < " + snumplayed

        ### filter opbouwen voor rating
        whererating = ""
        if 'srating0' in kwargs.keys():
            srating0 = kwargs['srating0']
            if srating0 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating0

        if 'srating1' in kwargs.keys():
            srating1 = kwargs['srating1']
            if srating1 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating1

        if 'srating2' in kwargs.keys():
            srating2 = kwargs['srating2']
            if srating2 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating2

        if 'srating3' in kwargs.keys():
            srating3 = kwargs['srating3']
            if srating3 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating3

        if 'srating4' in kwargs.keys():
            srating4 = kwargs['srating4']
            if srating4 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating4

        if 'srating5' in kwargs.keys():
            srating5 = kwargs['srating5']
            if srating5 != '':
                if len(whererating) > 0:
                    whererating = whererating + " or "
                whererating = whererating + " coalesce(songsinfo.rating, 0) = " + srating5

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
                dagen = timedelta(days=(4 * 7))
            if speriod == '8 weken':
                dagen = timedelta(days=(8 * 7))
            if speriod == '12 weken':
                dagen = timedelta(days=(12 * 7))
            if speriod == 'halfjaar':
                dagen = timedelta(days=(26 * 7))
            if speriod == 'jaar':
                dagen = timedelta(days=(52 * 7))

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
            select songs.song_id, songs.title, songs.year
                , songs.album, songs.album_id
                , songs.artist
                , songs.albumartist, songs.albumartist_id
                , songs.tracknumber
                , substr(min(to_char(playdate, 'yyyy-mm-dd')), 1, 10) as first
                , substr(max(to_char(playdate, 'yyyy-mm-dd')), 1, 10) as last
                , count(played.song_id) as played
                , coalesce(max(songsinfo.rating), 0) as rating
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
        # print 'query', query

        records = self.dbGetData(query)
        # print 'records', records

        h = mymc_html.pageSearchResult(records)

        return h


    def dbGetSongs(self, where="", having="", playdate="", artist="", period="", orderby=""):
        """Haal songs op, om te tonen in een table.
        In where, having, of playdate.
        Where en having moeten indien gebruikt geldige sql zijn.
        Playdate indien gebruik moet een datum zijn, met opmaak: yyyymmdd.
        """

        # geef gevonden records terug
        records = []

        # indien geen where of having opgegeven, dan terug
        if where == "" and playdate == "" and period == "":
            return records

        # bouw query op om gegevens op te halen (geen group bys omdat de details nodig zijn!)
        query = """
            select songs.song_id, songs.title, songs.artist, songs.year, songs.tracknumber
                , songs.album, songs.album_id
                , songs.albumartist, songs.albumartist_id
                , case when songsinfo.rating is null then 0 else songsinfo.rating end as rating
            from songs
            left join songsinfo
            on songs.song_id = songsinfo.song_id
            left join played
            on songs.song_id = played.song_id
        """

        # where, playdate
        playdate = str(playdate)
        if len(playdate) == 8:
            where = " to_char(played.playdate, 'yyyymmdd') = '%s' " % playdate
            orderby = " played.playdate "

        # where, period
        if period == 'lastday':
            where = " current_date - date(played.playdate) < 1 "
            orderby = " played.playdate "

        if len(where) > 0:
            where = ' where ' + where

        # sortering
        if orderby == "":
            orderby = " order by songs.year, songs.tracknumber "
        else:
            orderby = " order by " + orderby

        query = query + where + orderby
        # print 'query', query

        db = MyDB()
        records = db.dbGetData(query)
        # print 'records', records

        return records


    @cherrypy.expose
    def pageSearch(self):
        """Presenteer pagina om te zoeken.
        """

        h = mymc_html.pageSearch()

        return h
    

    @cherrypy.expose
    def sonosSetVolume(self, speaker=COORDINATOR, volume=10):
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

        # connectie met database maken
        db = MyDB()

        ## info over tabel songs
        query1 = """
        select 	count(distinct upper(albumartist)) as num_albumartist
        ,       count(distinct upper(albumartist || '#' || album)) as num_album
        ,       count(distinct upper(artist)) as num_artist
        ,       count(*) as num_song
        from songs
        """
        record1 = db.dbGetData(query1)
        # print "1: ", record1

        ## info over tabel played
        query2 = """
        select count(*) as num_played from played
        """
        record2 = db.dbGetData(query2)
        # print "2: ", record2

        ## info over hoeveel songs een rating hebben
        query3 = """
        select count(*) as num_songsinfo from songsinfo
        """
        record3 = db.dbGetData(query3)

        ## info over hoeveel songs in de queue zitten
        query4 = """
        select count(*) as num_queue from queue
        """
        record4 = db.dbGetData(query4)
        
        ## info over artists
        query5 = """
        select count(*) as num_tab_artists from artists
        """
        record5 = db.dbGetData(query5)
        
        ## info over albumartists
        query6 = """
        select count(*) as num_tab_albumartists from albumartists
        """
        record6 = db.dbGetData(query6)
        
        ## info over albums
        query7 = """
        select count(*) as num_tab_albums from albums 
        """
        record7 = db.dbGetData(query7)

        # één dictionary van maken
        record = dict(record1[0].items() + record2[0].items() + record3[0].items() + \
                      record4[0].items() + record5[0].items() + record6[0].items() + \
                      record7[0].items())
        print "record ", record

        h = mymc_html.pageInfoMc(record)

        return h
        

    @cherrypy.expose
    def pageListAlbums_AlbumArtist(self, albumartist_id="0"):
        """ageListAlbumArtists, alle album artiesten uitlijsten
        """

        # check of pagina in de cache bestaat
        pagename = "pageListAlbums_AlbumArtist"
        h = self.getFromCache(pagename, albumartist_id)
        if len(h) > 1:
            return h

        #albumartist='ABBA'
        # albumartist = q(albumartist)    # q(), voor namen als: Guys 'n' Dolls
        query = ("""
            select   album_id
            ,        min(albumartist) as albumartist
            ,        min(album) as album
            ,        min(year) as year
            ,        min(location) as location
            from     songs
            where    albumartist_id = %s
            group by album_id 
            order by year, album
        """ % int(albumartist_id))
        # print query
        
        hrecords = self.dbGetData(query)
        # print hrecords

        # haal template op en vul deze met gegevens
        h = mymc_html.pageListAlbums_AlbumArtist(hrecords)

        # sla pagina in cache op
        self.storeInCache(h, pagename=pagename, key1=albumartist_id)

        return h


    def createLinkFolderJpg(self, location=""):
        """createLinkFolderJpg, link maken naar folder.jpg bestand
        """
        if location != "":
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
        # print recordset

        hrecords = []
        tel = 0
        for record in recordset:
            hrecord = {}
            tel = tel + 1
            for sleutel in record.keys():
                hrecord[sleutel] = record[sleutel]
                if sleutel == u"location":
                    hrecord[u'folder_jpg'] = self.createLinkFolderJpg(hrecord[u'location'])
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


    @cherrypy.expose
    def pageListAlbumArtists(self):
        """ageListAlbumArtists, alle album artiesten uitlijsten
        """

        # gebruik pagina uit cache, als die bestaat
        pagename = u"pageListAlbumArtists"
        h = self.getFromCache(pagename)
        if len(h) > 1:
            return h

        db = MyDB()     # open database
        query = """
            select row_number() over (order by albumartist) as volgnr, albumartist, albumartist_id, num_songs, num_albums
            from (
                select albumartist, albumartist_id, count(*) as num_songs, count(distinct album) as num_albums
                from   songs
                group by albumartist, albumartist_id
                order by 1 ) as songs
        """
        # haal gegevens op
        hrecords = db.dbGetData(query)
        # voeg gegevens samen met template webpagina
        h = mymc_html.pageListAlbumArtists(hrecords)

        # sla pagina in cache op
        # 20140907, uit gezet: h = unicode(h, 'utf-8', errors='replace')
        self.storeInCache(h, pagename=pagename)
        
        return h

    @cherrypy.expose
    def pageSongSave(self, song_id=-1, rating=-1):
        """pageSongSave, pageSong submit verwerken en opslaan
        """

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
    def pageSong(self, song_id="0"):
        """Presenteer pagina om een song te raadplegen, en waardering op te geven.
        """

        # song_id = 1 # alleen waarde geven als debuggen

        # 1 - song gegevens ophalen
        song = self.dbGetSong(song_id)

        # 2 - afspeel info ophalen
        song_playinfo = dbGetSongInfoPlayed(song_id)
        if not song_playinfo:
            song_playinfo = {}
            song_playinfo['first'] = u"Never"
            song_playinfo['last'] = u"Never"
            song_playinfo['timesplayed'] = u"0"
        # print 'song_playinfo', song_playinfo

        # 3 - rating ophalen
        query = """
            select *
            from songsinfo
            where song_id = %s
        """ % int(song_id)
        song_info = self._db.dbGetData(query)
        if len(song_info) == 1:
            song_info = song_info[0]
        else:
            song_info = {}
            song_info['rating'] = 0
            song_info['notes'] = u""
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


    def dbGetSong(self, song_id=0):
        """dbGetSong, get a song record from the database with 1 song
        """

        ## controleer song_id
        if song_id < 1:
            return []
        
        # zoek de song op in de database
        query = """
            select *
            from songs
            where song_id = %s
            """ % int(song_id)
        records = self._db.dbGetData(query)

        if len(records) == 1:
            record = records[0]

            folder_jpg = "/muzik3" + record['location'] + "/" + 'folder.jpg'
            folder_jpg = urllib.quote(folder_jpg)
            folder_jpg = MCSERVER + folder_jpg
            record['folder_jpg'] = folder_jpg

            min = str(int(record['length'] / 60)) + ":"
            sec = str(record['length'] - int(record['length'] / 60) * 60)
            record['length'] = min + ((sec + "00")[0:2])

            # print 'dbGetSong record', record

        return record


    @cherrypy.expose
    def playAlsoSong2(self, song_id=0):
        """Song toevoegen aan de afspeeld lijst.
        Versie 2, om aan te roepen vanuit jquery.
        """

        song_id = int(song_id)

        query = """
            select * from songs where song_id = %s
        """ % song_id
        records = _db.dbGetData(query)
        
        # als song gevonden
        if len(records) == 1:
            record = records[0]
            ## uri samenstellen van de song
            uri = "/muzik3" + record['location'] + "/" + record['filename']
            print uri

            ## stuur nummer naar sonos
            sonos = SoCo(COORDINATOR)
            # zonder encode werkte niet voor bijvoorbeeld: Nånting Är På Väg
            uri = urllib.quote(uri).encode('utf8')
            uri = MCSERVER + uri
            # print uri
            sonos.add_uri_to_queue(uri)

            ## log song als afgespeeld
            ############### eerst testen, daarna pas logging aan ###################
            # TODO: testen !
            # dbLogPlayedSong()
            
            # stop song_id in queue table
            query = """
                insert into queue (song_id) values (%s) 
            """ % song_id
            _db.dbExecute(query)


    @cherrypy.expose
    def playAlsoSong(self, song_id=0):
        """playAlsoSong, nummer toevoegen aan afspeellijst, met: add_uri_to_queue(uri)
        """
        
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
        # print uri
        # print type(uri)

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
        # zonder encode werkte niet voor bijvoorbeeld: Nånting Är På Väg
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
    def listAlbumTracks(self, album_id="0"):
        """Toon alle songs van een album.
        """

        # indien pagina in cache, gebruik die dan
        pagename = "listAlbumTracks"
        h = self.getFromCache(pagename, album_id)
        if len(h) > 1:
            return h
        
        # haal tracks op
        query = """
            select * from songs where album_id = %s order by tracknumber
        """ % int(album_id)
        records = self._db.dbGetData(query)
        
        # pagina samenstellen, met records en template
        h = mymc_html.listAlbumTracks(album_id, records)

        # pagina opslaan in cache
        self.storeInCache(h, pagename=pagename, key1=album_id)

        return h


    @cherrypy.expose
    def pageSoftwareVersions(self):
        """Toon software versies
        """

        records = {}
        # python versie
        records['python'] = sys.version
        # cherrypy versie
        records['cherrypy'] = cherrypy.__version__
        # soco (sonos) versie
        records['soco'] = soco.__version__

        h = mymc_html.pageSoftwareVersions(records)

        return h


    @cherrypy.expose
    def pageAboutMe(self):
        """pagina over deze applicatie
        """

        records = {}
        records['info'] = """
            MC, Music Collection <br>
            <br>
            Python applicatie om muziek collectie te beheren. <br>
            - uniek nummeren muziek nummers <br>
            - laden in postgres database <br>
            - afspelen van de muziek op Sonos systeem <br>
            - bijhouden wat afgespeeld is, en wanneer <br>
            - rating (0-5 punten) muziek nummers <br>
            - vrij zoeken <br>
            - zoeken met selecties <br>
            - zoeken met super selecties <br>
        """

        h = mymc_html.pageAboutMe(records)

        return h


    def dbExecute(self, query):
        """Voer queries uit, niet om gegevens op te halen, maar data manipulatie,
        zoals inserts, deletes, etc"""
    
        self.dbOpen()
        Mc.cursor.execute(query)
        # print 'query', query
        Mc.connection.commit()
        self.dbClose()
    
    
    def dbOpen(self):
        """open connection met de database
        """
        
        if Mc.connection is None:
            ### postgresql
            try:
                Mc.connection = psycopg2.connect(database=DBNAME, \
                    user=DBUSER, host=DBHOST, port=DBPORT)
                # gewone cursor
                # Mc.cursor = Mc.connection.cursor()
                # dictionary cursor
                Mc.cursor = Mc.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                Mc.cursor.execute('select version()')
                ver = Mc.cursor.fetchone()
                print ver
    
            except psycopg2.DatabaseError, e:
                print 'Error %s' % e
    
        return True
    
    
    def dbClose(self):
        """ database cursor en connectie sluiten
        """
    
        return
    
        try:
            if not Mc.cursor.closed:
                Mc.cursor.close()
            if not Mc.connection.close:
                Mc.connection.close()
    
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e


def debug(input):
    """print debug meldingen
    """
    if DEBUG:
        print input


if __name__ == '__main__' and not 'idlelib.__main__' in sys.modules:
    conf = {
         '/': {
             'tools.staticdir.root': os.path.abspath(os.getcwd()),
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': '../public'
         }
     }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8081,
    })

    root = Mc()
    root.queuebeheer = queuebeheer.queuebeheer.queuebeheer()
    root.pageSelections = selections.selections.pageSelections()
    root.pageSearchWithSelections = searchwithselections.searchwithselections.searchWithSelections()
    
    cherrypy.quickstart(root, '/', conf)

