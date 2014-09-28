# -*- coding: utf-8 -*-

"""Module queue.

Bevat class afspeel queue te beheren.

"""


__author__  = 'dp'
__date__    = '2014-09'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


import cherrypy             # cherrypy de webinterface
from soco import SoCo       # sonos

import queuebeheer_temp
reload(queuebeheer_temp)
from dbfunc import MyDB
from dbfunc import q

# COORDINATOR = sonos_discover.getSonosCoordinator()
COORDINATOR = '192.168.1.21'


class queuebeheer(object):
    """Class om afspeel queue te beheren.
    """


    def __init__(self):
        """Database verbinding maken.
        @ivar _db: database  
        """
        self._db = MyDB() 


    @cherrypy.expose
    def index(self):
        """sonos_menu, menu om commando's aan sonos te geven en info op te halen
        """

        # verbinding maken met sonos
        sonos = SoCo(COORDINATOR)

        # wat speelt er nu, als het nummer niet uit playlist komt, is current_track niet gevuld
        current_song = sonos.get_current_track_info()
        current_track = int(current_song['playlist_position'])

        # haal queue uit database op
        query = """select * from queue order by queue_id"""
        records = self._db.dbGetData(query)
        # print 'queue records', records

        # haal pagina op
        h = queuebeheer_temp.sonos_playmenu(records, sonos, current_track)

        return h


    @cherrypy.expose
    def sonos_next(self):
        """Afspeellijst <Next> button, gaat naar volgende nummer in afspeellijst.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_next()
                
        ##
        sonos = SoCo(COORDINATOR)
        sonos.next()

        return h


    @cherrypy.expose
    def sonos_previous(self):
        """Afspeellijst, <Previous> button, gaat naar vorige nummer, in de afspeellijst.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_previous()
                
        ##
        sonos = SoCo(COORDINATOR)
        sonos.previous()

        return h


    @cherrypy.expose
    def sonos_pause(self):
        """Afspeellijst, <pause> button, afspelen pauzeren.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_pause()
                
        ## sonos, afspelen pauzeren
        sonos = SoCo(COORDINATOR)
        sonos.pause()

        return h


    @cherrypy.expose
    def sonos_clear_queue(self):
        """sonos_clear_queue, maak sonos afspeellijst leeg
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_clear_queue()
                
        ## queue leegmaken als er wat in zit
        sonos = SoCo(COORDINATOR)
        # als de sonos queue niet leeg is
        if len(sonos.get_queue()) > 0:
            ## sonos queue leegmaken
            sonos.clear_queue()

            query = """
                delete from queue
            """
            self._db.dbExecute(query)

        return h


    @cherrypy.expose
    def sonos_play_from_queue(self):
        """sonos_play_from_queue, speelt queue af
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_play_from_queue()

        # queue afspelen als deze niet leeg is
        sonos = SoCo(COORDINATOR)
        if len(sonos.get_queue()) > 0:
            sonos.play_from_queue(0)

        return h


    @cherrypy.expose
    def sonos_play(self):
        """Afspeellijst, <play> button, afspelen of doorgaan na een pauze.
        """
        
        # pagina laden voor als antwoord terug aan de server
        h = queuebeheer_temp.sonos_play()
                
        ## sonos, afspelen
        sonos = SoCo(COORDINATOR)
        sonos.play()

        return h
