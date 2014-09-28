# -*- coding: utf-8 -*-

"""Deze module hoort bij module mymc.

Deze module bevat templates en functies om webpagina's
te genereren. 

"""

__author__  = 'dp'
__date__    = '2014-09'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


import os
import urllib           # vertaal string naar url

from htable import hTable
from hTable import Html
from hTable import hLink, hButton
from hTable import TDO, TDC, TRO, TRC, TABO, TABC

from mymc_html import html_start
from mymc_html import main_navigation
from mymc_html import html_page
from mymc_html import html_h1
from mymc_html import html_end


def sonos_playmenu(records, sonos, current_track):
    """Geef webpagina terug om afspeellijst (queue) te beheren.
    
    De queue kan afgespeeld en leeggemaakt worden. Tevens zijn er knoppen 
    voor previous, next, stop en pause.
    Oude naam: sonos_menu.
    """

    title = "sonos_playmenu" 
    h = html_start(title) + main_navigation() + html_h1("Queue beheer")
    
    tab1 = hTable()
    tab1.td(hButton(u'Previous'    , u'btn1', u'menuknop', u'sonos_previous'))
    tab1.td(hButton(u'Pause'       , u'btn2', u'menuknop', u'sonos_pause'))
    tab1.td(hButton(u'Play'        , u'btn3', u'menuknop', u'sonos_play'))
    tab1.td(hButton(u'Next'        , u'btn4', u'menuknop', u'sonos_next'))
    tab1.td(hButton(u'Clear queue' , u'btn5', u'menuknop', u'sonos_clear_queue'))
    tab1.td(hButton(u'Play queue'  , u'btn6', u'menuknop', u'sonos_play_from_queue'))


    # list songs in sonos queue
    tab2 = hTable()
    if len(sonos.get_queue()) > 0:
        tab2.insert("""
            <h2>Sonos queue</h2>""")

        tab2.add("""<tr> <th class="info">Info</th> 
            <th class="track">Track</th> <th class="title">Titel</th>  
            <th class="artist">Artiest</th> <th class="album">Album</th></tr>""")
        tel = 0
        for song in sonos.get_queue():
            tel = tel + 1
            tab2.add(TRO)

            tab2.add('<td class="info">')
            if (tel - 1) < len(records):
                record = records[tel - 1]
                song_id = record['song_id']
                tab2.add('<a href="/pageSong?song_id=%s">Info</a>' % song_id)
            tab2.add("</td>")
                
            if tel == current_track:
                tab2.add('<td class="track">' + ">" + str(tel) + "< </td>")
            else:
                tab2.add('<td class="track">' + str(tel) + "</td>")

            tab2.add('<td class="title">' + song.title + "</td>")
            # gegevens kunnen None zijn als de sonos server de gegevens nog niet heeft opgehaald
            if song.creator is None:
                tab2.add('<td class="artist">' + "</td>")
            else:
                tab2.add('<td class="artist">' + song.creator + "</td>")
                
            if song.album is None:
                tab2.add('<td class="album">' + "</td>")
            else:
                tab2.add('<td class="album">' + song.album + "</td>")

            tab2.add(TRC)
            
    h = h + html_page(tab1.exp() + tab2.exp()) + html_end()
    
    return h


def sonos_next():
    """Dummy pagina voor de next button.
    """
    
    return u"""
    <html>
    sonos_next</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


def sonos_previous():
    """Dummy pagina voor de previous button.
    """
    
    return u"""
    <html>
    sonos_previous</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


def sonos_play():
    """Dummy pagina voor de play button.
    """
    
    return u"""
    <html>
    sonos_play</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


def sonos_pause():
    """Dummy pagina voor de pause button.
    """
    
    return u"""
    <html>
    sonos_pause</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


def sonos_clear_queue():
    """Dummy pagina voor clear queue button.
    """
    
    return u"""
    <html>
    sonos_clear_queue</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


def sonos_play_from_queue():
    """Dummy pagina voor button play from queue.
    """
    
    return u"""
    <html>
    sonos_play_from_queue</br>

    <script>
        window.history.back();
    </script>

    </html>
"""


