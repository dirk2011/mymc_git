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


# import cherrypy         # cherrypy de webinterface
import os
# import json
import urllib           # vertaal string naar url
# import cgi

from htable import hTable
from hTable import Html
from hTable import hLink, hButton
from hTable import TDO, TDC, TRO, TRC, TABO, TABC


def html_start(title):
    """Begin van een html pagina, head t/m body, inclusief laden stylesheet.
    """
    # 2014-08-30, creatie

    return u"""<!DOCTYPE html>
<html>
<head>
<title>%(title)s</title>
<link rel="stylesheet" type="text/css" href="/static/css/style.css">
<script src="/static/js/jquery.js" type="text/javascript"></script>
</head>
<body>""" % {'title': title}


def html_end():
    """Einde van een pagina.
    """

    return u"""
</div></body></html>"""


def html_h1(text):
    """Return h1 element with passed text.
    """

    return u"""
    <div id="kop"> <h1 id="kop_tekst">%(text)s</h1> </div>
    """ % {'text': text}


def html_page(page):
    """Geef pagina terug in div pagina,
    er kan gescrolled worden, en kop blijft staan. 
    """

    return u"""
    <div id="top">
    </div>
    <div id="pagina">
    """ + page + """
    </div>"""


def main_navigation():
    """Menu voor de website.
    """

    h = hTable()
    h.td(hButton(u'Home', u'btnHome', u'menuknop', u'/index'))
    h.td(hButton(u'Info Mc', u'btnInfoMc', u'menuknop', u'/pageInfoMc'))
    h.td(hButton(u'Artiesten', u'btnArtiesten', u'menuknop', u'/pageListAlbumArtists'))
    h.td(hButton(u'Zoeken', u'btnZoeken', u'menuknop', u'/pageMenuSearch'))
    h.td(hButton(u'Queue', u'btnQueue', u'menuknop', u'/sonos_playmenu'))
    h.td(hButton(u'Volume', u'btnVolume', u'menuknop', u'/pageSonosSpeakers'))
    h.td(hButton(u'Afgespeeld', u'btnAfgespeeld', u'menuknop', u'/pageAfgespeeld'))
    h.td(hButton(u'Beheer', u'btnBeheer', u'menuknop', u'/pageBeheer'))
    h.closeall()

    return u"""<div id="kopmenu">%s</div> """ % h.exp()


def linkpageAlbumArtist(albumartist, albumartist_id):
    """geef link terug: href naar album artist
    """

    return u"""<a href=pageListAlbums_AlbumArtist?albumartist_id=%s>""" % albumartist_id \
        + albumartist + u"</a>"


def linkpageAlbumTracks(album, album_id):
    """geef link terug: href naar album_id
    """

    return u"""<a href=listAlbumTracks?album_id=%s>""" % album_id + album + u"</a>"


def linkpageSong(song_id):
    """geef link terug: href naar song info pagina
    """

    song_id = str(song_id)
    link = urllib.quote(song_id)
    return u"""<a href=pageSong?song_id=%s>""" % link + song_id + u"</a>"


def pageSong():
    """Geef webpagina terug, met veel gegevens over een song.

    Input voor de mymc module is song_id.
    Terug door deze functione, de html pagina.
    """

    title = u'pageSong'
    return html_start(title) + main_navigation() + html_h1(u'Liedje pagina') +  \
        html_page(u"""

<table><tr><td>
<fieldset>

<table>
  <tr>
    <td>
      <img src="%(folder_jpg)s" height="300" width="300">
    </td>

    <td valign="TOP">
      <fieldset><legend>Played info</legend>
    <table>
      <tr><td>
        Played
      </td><td>
        %(timesplayed)s
      </td></tr><tr><td>

        First time
      </td><td>
	    %(first)s
	  </tr></tr><tr><td>

	    Last time
	  </td><td>
	    %(last)s
	  </td></tr><tr><td>

	    Rating
	  </td><td>
	    %(rating)s
	  </td></tr>
	</table>
      </fieldset>
    </td>
  </tr>

  <tr>
    <td colspan="2">
    <fieldset><legend>Song / Track info</legend>

<table>
    <tr><td>
	  ID
	</td><td>
	  %(song_id)s

	</td></tr><tr><td>
	  Titel
	  </td><td>
	  %(title)s

	</td></tr><tr><td>
	  Artiest
	</td><td>
	  %(artist)s

	</tr></tr><tr><td>
	  Lengte
	</td><td>
	  %(length)s

	</tr></tr><tr><td>
	  Album
	</td><td>
	  <a href="listAlbumTracks?album_id=%(album_id)s"> %(album)s </a>

	</td></tr><tr><td>
	  Track
	</td><td>
	  %(tracknumber)s

	</td></tr><tr><td>
	  Albumartiest
	</td><td>
        <a href="pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s"> %(albumartist)s </a>

	</td></tr><tr><td>
	  Jaar
	</td><td>
	  %(year)s

	</td></tr><tr><td>
        Bitrate
	</td><td>
        %(bitrate)s

	</td></tr><tr><td>
        Size
	</td><td>
        %(size)s (Mb's)

    </td></tr><tr><td class="song_bestand_label">
        Bestand
    </td><td class="song_bestand_data">
        %(filename)s

    </tr></td>

</table>
</fieldset>

  </td>
</tr>
<tr>
  <td colspan="2">
    <fieldset><legend>Input</legend>
    <table>
    <tr>
      <td>
	<form action="pageSongSave">
	  Rating: 
	  <input type="radio" name="rating" value="0" checked>0 &nbsp; &nbsp;
	  <input type="radio" name="rating" value="1">1 &nbsp; &nbsp;
	  <input type="radio" name="rating" value="2">2 &nbsp; &nbsp;
	  <input type="radio" name="rating" value="3">3 &nbsp; &nbsp;
	  <input type="radio" name="rating" value="4">4 &nbsp; &nbsp;
	  <input type="radio" name="rating" value="5">5
	  <br><br>
	  <input type="submit" value="Ok">
	  <input type="text" hidden name="song_id" value="%(song_id)s">
	  <!-- <input type="submit" value="Cancel"> -->
	</form>
      </td>
    </tr>
    </table>
    </fieldset>
  </td>
</tr>

</table>
""") + html_end()


def sonos_playmenu():
    """Geef webpagina terug om afspeellijst (queue) te beheren.
    
    De queue kan afgespeeld en leeggemaakt worden. Tevens zijn er knoppen 
    voor previous, next, stop en pause.
    Oude naam: sonos_menu.
    """

    title = "sonos_playmenu" 
    h = html_start(title) + main_navigation() + html_h1("Queue beheer")
    
    table = hTable()
    
    table.td(TDO + """
        <form action="sonos_previous">
        <input type="submit" value="Previous">
        </form>
        """ + TDC)
    
    table.td(TDO + """
        <form action="sonos_pause">
        <input type="submit" value="Pause">
        </form>
    """ + TDC)
    
    table.td(TDO + """
        <form action="sonos_play">
        <input type="submit" value="Play">
        </form>
    """ + TDC)

    table.td(TDO + """
        <form action="sonos_next">
        <input type="submit" value="Next">
        </form>
    """ + TDC)

    table.td(TDO + """
        <form action="sonos_clear_queue">
        <input type="submit" value="Clear queue">
        </form>
    """ + TDC)

    table.td(TDO + """
        <form action="sonos_play_from_queue">
        <input type="submit" value="Play queue">
        </form>
    """ + TDC)

    return h + html_page(table.exp())


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


sonos_clear_queue = u"""
    <html>
    sonos_clear_queue</br>

    <script>
	    window.history.back();
    </script>

    </html>
"""


sonos_play_from_queue = u"""
    <html>
    sonos_play_from_queue</br>

    <script>
	    window.history.back();
    </script>

    </html>
"""


pageSongSave = u"""
    <html>
    pageSongSave</br>

    <script>
	    window.history.back();
    </script>

    </html>
"""


def pageListAlbumArtists(records):
    """
    Toon de artiesten die één of meerdere albums hebben.
    Input: list bestaande uit dictionaries, dictionary: volgnr, albumartist, num_songs, num_albums
    Output: html string
    """

    title = u'pageListAlbumArtists'
    h = html_start(title) + main_navigation() + html_h1(u'Album artiesten')

    # table data
    h_td = u"""
    <td >
      
    </td><td class="ListAlbumArtists">
      <a href="pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s">%(albumartist)s</a><br>
      %(volgnr)s / %(num_albums)s / %(num_songs)s
    </td>"""

    table = hTable()    # begin met opbouw tabel
    
    # doorloop alle records
    tel = 0
    for record in records:
        # print 'record', record
        tel = tel + 1
	
        if tel == 1:
            table.add(TRO)
	
        print 'record', record
        table.add(h_td % record)
	
        if tel == 4:
            table.add(TRC)
            tel = 0

    if tel != 0:
        table.add(TRC)

    h = h + html_page(table.exp()) + html_end()
    
    return h


def testPageListAlbumArtists():
    """Functie voor het testen van pageListAlbumArtists() met dummy data.
    """
    
    record1 = {'volgnr': 1, 'albumartist': 'ABBA  ', 'num_songs': 63, 'num_albums': 5}
    record2 = {'volgnr': 1, 'albumartist': 'B ABBA', 'num_songs': 63, 'num_albums': 5}
    record3 = {'volgnr': 1, 'albumartist': 'C ABBA', 'num_songs': 63, 'num_albums': 5}
    record4 = {'volgnr': 1, 'albumartist': 'D ABBA', 'num_songs': 63, 'num_albums': 5}
    record5 = {'volgnr': 1, 'albumartist': 'E ABBA', 'num_songs': 63, 'num_albums': 5}
    records = [record1, record2, record3, record4, record5]

    h = pageListAlbumArtists(records)
    print h

    return h

    
def testPageListAlbums_AlbumArtist():
    """Functie voor het testen van functie: pageListAlbums_AlbumArtist, met dummy data.
    """
    record1 = {'albumartist': 'Bee Gees', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record2 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record3 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record4 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record5 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    records = [record1, record2, record3, record4, record5]

    h = pageListAlbums_AlbumArtist(records)
    # print h

    return h


def pageInfoMc(record):
    """Toon aantallen uit de mc database.
    """
    
    title = 'pageInfoMc'
    page = html_start(title) + main_navigation() + html_h1(u'Info over mijn muziekcollectie (mc)') 

    dt = u"""
    <table>
        <tr class="ExtraHoog">
            <td> Table songs </td><td> %(num_song)s </td>
        </tr><tr class="ExtraHoog">
            <td> <a href="pageListAlbumArtists">Album artiesten </a> </td>
            <td> %(num_albumartist)s upper() </td>
        </tr><tr class="ExtraHoog">
            <td> Albums 	    </td><td> %(num_album)s upper() </td>
        </tr><tr class="ExtraHoog">
            <td> Artiesten 	    </td><td> %(num_artist)s upper() </td>
        </tr><tr class="ExtraHoog">
            <td> Table played    </td><td> %(num_played)s </td>
        </tr><tr class="ExtraHoog">
            <td> Table songsinfo </td><td> %(num_songsinfo)s (songs met een rating) </td>
        </tr><tr class="ExtraHoog">
            <td> Table queue     </td><td> %(num_queue)s (songs in afspeel queue) </td>

        </tr><tr class="ExtraHoog">
            <td> Table albumartists  </td><td> %(num_tab_albumartists)s </td>
        </tr><tr class="ExtraHoog">
            <td> Table albums        </td><td> %(num_tab_albums)s </td>
        </tr><tr class="ExtraHoog">
            <td> Table artists       </td><td> %(num_tab_artists)s </td>
        </tr>
    </table>
"""

    page = page + html_page(dt % record) + html_end()
    
    return page


def pageSonosSpeakers(records):
    """Geef web pagina terug, om volume van de speakers te beheren.
    Tevens geeft dit inzicht in alle sonos componenten.
    """

    title = u'pageSonosSpeakers' 
    h = html_start(title) + main_navigation() + html_h1(u'Sonos boxen')
    
    h_td = u"""
    <td class="SonosSpeakers">%(zone_name)s</td>
    <td class="SonosSpeakers">%(mute)s</td>
    <td class="SonosSpeakers">%(volume)s</td>
    <td class="SonosSpeakers">
      <table>
	    <tr>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=0">0</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=10">10</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=15">15</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=20">20</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=25">25</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=30">30</td>

	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=40">40</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=50">50</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=60">60</td>
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=70">70</td>
	    </tr>
      </table>
    </td>

    <td class="SonosSpeakers">%(volgnr)s</td>
    <td class="SonosSpeakers">%(ip_address)s</td>
    <td class="SonosSpeakers">%(is_coordinator)s</td>
<!--    <td>%(is_speaker)s</td>
    <td>%(loudness)s</td>
    <td>%(treble)s</td>
    <td>%(bass)s</td>
    <td>%(status_light)s</td> -->

    """

    h_page_c = u"""
<p>Pagina laden duurt even, omdat bij iedere box gegevens worden opgehaald.</p>
<p>Ververs de pagina om actuele volume gegevens te zien.</p>
"""

    h_page_o = u"""
<table border="1">
    <tr><th class="SonosSpeakers">Naam</th>
        <th class="SonosSpeakers">Aan/Uit</th>
        <th class="SonosSpeakers">Volume</th> 
        <th class="SonosSpeakers">Zet volume</th>
        <th class="SonosSpeakers">Component</th>
        <th class="SonosSpeakers">Adres</th>
        <th class="SonosSpeakers">Coordinator</th>
    </tr>
"""

    # begin van de pagina
    h_page = h_page_o

    # doorloop alle records
    for record in records:
        # print 'record', record
        h_page = h_page + TRO
	
        h_page = h_page + (h_td % record)
	
        h_page = h_page + TRC

    h_page = h_page + TABC + h_page_c

    h = h + html_page(h_page) + html_end()
    # print len(h)

    return h


def testPageSonosSpeakers():
    """Functie voor het testen van functie: pageSonosSpeakers met dummy data.
    """
    records = [{'volgnr': 1, 'treble': '', 'bass': '', 'mute': '', 'status_light': False,
                'is_speaker': False, 'volume': '', 'is_coordinator': False, 'loudness': '',
                'zone_name': 'BRIDGE', 'ip_address': '192.168.1.13'},
               {'volgnr': 2, 'treble': 0, 'bass': 0,
                'mute': False, 'status_light': True, 'is_speaker': True, 'volume': 15, 'is_coordinator': True,
                'loudness': True, 'zone_name': 'Huiskamer (L)', 'ip_address': u'192.168.1.19'},
               {'volgnr': 3,
                'treble': 0, 'bass': 0, 'mute': False, 'status_light': True, 'is_speaker': True, 'volume': 15,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Huiskamer (R)',
                'ip_address': u'192.168.1.18'},
               {'volgnr': 4, 'treble': 0, 'bass': 0, 'mute': False, 'status_light': True, 'is_speaker': True, 'volume': 15,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Huiskamer (S)', 'ip_address': u'192.168.1.12'},
               {'volgnr': 5, 'treble': 0, 'bass': 0, 'mute': True, 'status_light': True, 'is_speaker': True, 'volume': 0,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Slaapkamer (L)', 'ip_address': u'192.168.1.20'},
               {'volgnr': 6, 'treble': 0, 'bass': 0, 'mute': True, 'status_light': True, 'is_speaker': True, 'volume': 0,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Slaapkamer (R)', 'ip_address': u'192.168.1.15'},
               {'volgnr': 7, 'treble': 0, 'bass': 0, 'mute': False, 'status_light': True, 'is_speaker': True, 'volume': 45,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Studeerkamer (L)', 'ip_address': u'192.168.1.21'},
               {'volgnr': 8, 'treble': 0, 'bass': 0, 'mute': False, 'status_light': True, 'is_speaker': True, 'volume': 45,
                'is_coordinator': False, 'loudness': True, 'zone_name': 'Studeerkamer (R)', 'ip_address': u'192.168.1.16'}]
    # print records

    h = pageSonosSpeakers(records)
    print h


def sonosSetVolume(record):
    """Dummy html pagina, de mymc functie past het volume aan van de gevraagde speaker.
    
    In dictionary, met 2 waarden: speaker en volume, kan hier voor debuggen worden
    weergegeven. 
    """

    return u"""
    <html>
    sonosSetVolume</br>

    <script>
        window.history.back();
    </script>

    <form>
        <input type="text" name="speaker" value="%(speaker)s">
        <input type="text" name="volume"  value="%(volume)s">
    </form>

    </html>
    """ % record


def pageIndex():
    """Index (start) pagina van mymc.
    """
    
    page = u"""
    
    <img src="/static/images/music_017.jpg">

    """
    title = u'pageIndex'
    h_page = html_start(title) + main_navigation() + html_h1(u'My Music Collection') + html_page(page) + html_end()
    
    return h_page


def pageSearch():
    """Pagina om te zoeken in de muziek collectie.
    """
  
    title = u'pageSearch'
    return html_start(title) + main_navigation() + html_h1(u'Tracks zoeken') + html_page(u"""
<form action="pageSearchResult">
<table>
<tr><td>

<fieldset><legend>Song eigenschappen</legend>
<table>
  <tr>
    <td colspan="2">Vul alleen velden in waarop gezocht moet worden.</td>
  </tr><tr>
    <td>Albumartiest</td>
    <td><input type="text" name="salbumartist" size="50"></td>

  </tr><tr>
    <td>Artiest</td>
    <td><input type="text" name="sartist" size=50>Geen auto %.</td>

  </tr><tr>
    <td>Album</td>
    <td><input type="text" name="salbum" size=50></td>

  </tr><tr>
    <td>Titel</td>
    <td><input type="text" name="stitle" size=50></td>
    
    <!--
    <td>Sleutel woorden</td>
    <td>
	  <select name="keywords" multiple size=6>
	  <option value="1">female</option>
	  <option value="2">male</option>
	  <option value="3">group</option>
	  <option value="4">country</option>
	  <option value="5">soul</option>
	  <option value="6">pop</option>
	  </select>
	  -->
    </td>
  </tr><tr>
    <td>Jaar</td>
    <td><input type="numeric" name="syear" size=4></td>
    <!-- <td><input type="date" name="dat" id="dat"></td> -->
  </tr>
</table>
</fieldset>

</td></tr><tr><td>

<fieldset><legend>Andere eigenschappen</legend>
<table>
  <tr>
    <td>Minder dan keer</td>
    <td><input type="numeric" name="snumplayed" size=4>afgespeeld</td>

  </tr><tr>
    <td>Niet afgespeeld laatste</td>
    <td>
      <select name="speriod" size=6>
	<option value="week">week</option>
	<option value="4 weken">4 weken</option>
	<option value="8 weken">8 weken</option>
	<option value="12 weken">12 weken</option>
	<option value="halfjaar">halfjaar</option>
	<option value="jaar">jaar</option>
      </select>
    </td>
  </tr><tr>
    <td>Waardering</td>
    <td>
      <input type="checkbox" name="srating0" value="0">0
      <input type="checkbox" name="srating1" value="1">1
      <input type="checkbox" name="srating2" value="2">2
      <input type="checkbox" name="srating3" value="3">3
      <input type="checkbox" name="srating4" value="4">4
      <input type="checkbox" name="srating5" value="5">5
    </td>
  </tr>
</table>
</fieldset>
  
</tr><tr>
  <td colspan="2">Het zoek resultaat geeft een maximum aantal terug.</td>
</tr><tr>
  <td><button type="submit" name="zoeken">Zoeken</button></td>
</tr>
   
</table>
</form>
    """) + html_end()


def pageSearchResult(records):
    """Pagina om het zoek resultaat te tonen.
    """

    title = u'pageSearchResult'
    h = html_start(title) + main_navigation() + html_h1(u'Zoek resultaat')
    
    h_tr_h = u"""
<tr>
    <th>Info</th>
    <th>#</th>
    <th>Titel (link voeg toe aan wachtrij)</th>
    <th>Artiest</th>
    <th>Album /
        Rating /
        Jaar /
        Gespeeld /
        Laatst</th>
</tr>
"""

    h_td = u"""
<tr>
    <td class="info" rowspan="2">
        <a href="pageSong?song_id=%(song_id)s">Info</a>
    </td>
  
    <td class="track" rowspan="2">
        %(volgnr)s
    </td>
  
    <td class="title" rowspan="2">
        <a href="playAlsoSong?song_id=%(song_id)s">
        %(title)s
        </a>
    </td>

    <td class="artist" rowspan="2">
        <a href="pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s">
        %(artist)s
        </a>
    </td>

    <td class="album">
        <a href="listAlbumTracks?album_id=%(album_id)s">
        %(album)s
        </a>
    </td>
</tr>
<tr>
    <td colspan="1">
        %(rating)s / %(year)s / %(played)s / %(last)s  
    </td>
</tr>
"""

    h_page = Html()
    h_page.add(TABO)

    if len(records) == 0:
        h_page.add(u"""<br>Geen gegevens gevonden die aan de selectie voldoen.<br>
            Probeer het opnieuw.""")
    else:
        h_page.add(h_tr_h)
        for record in records:
            h_page.add(h_td % record)

    h_page.add(TABC)
    
    h = h + html_page(h_page.exp()) + html_end()

    return h


def pageClearCache(records):
    """Pagina, voor als op clear cache is gedrukt.
    Er wordt een overzicht getoond van verwijderde pagina's uit de cache.
    """

    title = u'pageClearCache'
    h = html_start(title) + main_navigation() + html_h1(u'Clear Cache') 

    h_td = u"""%(regel)s"""
    
    table = hTable()
    if len(records) > 0:
        table.td(u"""De volgende pagina's zijn verwijderd.</td>""")
        for record in records:
            table.tr()
            table.td(h_td % {'regel': record})
    else:
        table.tr()
        table.td(u"""Er zijn geen pagina's in cache gevonden. """)

    h = h + html_page(table.exp()) + html_end()

    return h


def pageShowCache(records):
    """Toon pagina's in cache.
    """

    title = u'pageShowCache'
    h = html_start(title) + main_navigation() + html_h1(u"Pagina's in cache") 

    h_td = u"""%(volgnr)s: %(bestand)s"""
    
    table = hTable()
    if len(records) > 0:
        table.td(u"""De volgende pagina's bevinden zich in de cache.</td>""")
        # print records
        for record in records:
            table.tr()
            table.td(h_td % record)
    else:
        table.tr()
        table.td(u"""Er zijn geen pagina's in cache gevonden. """)

    h = h + html_page(table.exp()) + html_end()

    return h


def pagePartSongRating(song_id, rating):
    """Stukje html etc, voor rating van songs, om in te voegen in andere pagina's,
       nodig: song_id, en huidige rating.
    """

    h_page = u"""
<!-- <table>
  <tr>
    <td>  -->
      <form action="partSongRatingSave">
	  Rating: 
	  <input type="radio" name="rating" value="0" %(checked0)s>0
	  <input type="radio" name="rating" value="1" %(checked1)s>1
	  <input type="radio" name="rating" value="2" %(checked2)s>2
	  <input type="radio" name="rating" value="3" %(checked3)s>3
	  <input type="radio" name="rating" value="4" %(checked4)s>4
	  <input type="radio" name="rating" value="5" %(checked5)s>5
	  <input type="text" hidden name="song_id" value="%(song_id)s">
	  <input type="submit" value="Save" action="partSongRatingSave">
      </form>
<!--    </td>
  </tr>
</table> -->

    """

    record = {}
    record[u'song_id'] = song_id
    record[u'checked0'] = u"checked" if rating == 0 else u""
    record[u'checked1'] = u"checked" if rating == 1 else u""
    record[u'checked2'] = u"checked" if rating == 2 else u""
    record[u'checked3'] = u"checked" if rating == 3 else u""
    record[u'checked4'] = u"checked" if rating == 4 else u""
    record[u'checked5'] = u"checked" if rating == 5 else u""

    h = (h_page % record)

    return h


def testPagePartSongRating():
    """ Testen pagePartSongRating
    """
    
    song_id = 999
    rating = 5
    h = pagePartSongRating(song_id, rating)

    return h


def pageBeheer():
    """Pagina voor beheer, verversen en opschonen, van tabellen, pagina's.
    """

    title = 'pageBeheer'
    h = html_start(title) + main_navigation() + html_h1("Beheer") 
    
    table = hTable()
    link = hLink(u"Selecties muteren", u"pageSelections")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Toon pagina's in cache", u"pageShowCache")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Clear cache, verwijder gegenereerde webpagina's.", u"pageClearCache")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Ververs played history", u"pageRefreshPlayedHistory")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Ververs played artists", u"pageRefreshPlayedArtists")
    table.td(link, u'beheer')
    table.tr()
    
    return h + html_page(table.exp()) + html_end()


def pageRefreshPlayedHistory():
    """pageRefreshPlayedHistory, cijfers verversen voor played history.
    """

    title = u'pageRefreshPlayedHistory'
    h = html_start(title) + main_navigation() + html_h1(title) + html_page(u"""

    <script>
        window.history.back();
    </script>

""") + html_end()

    return h


def pageRefreshPlayedArtists():
    """pageRefreshPlayedArtists, cijfers verversen voor played artists.
    """

    title = u'pageRefreshPlayedArtists'
    h = html_start(title) + main_navigation() + html_h1(title) + html_page("""
    
    <script>
        window.history.back();
    </script>
    """) + html_end() 

    return h

    
def pagePlayedHistory(yearsdict, monthsdict, daysdict):
    """Toon webpagina met afspeel resultaten per jaar, maand, dag,
    met doorklik naar ander jaar en maand.
    """

    title = u'pagePlayedHistory'
    h = html_start(title) + main_navigation() + html_h1(u'Afgespeeld per periode')

    # deel 1, jaren
    h_part1_d = u"""
    <h2>Jaren</h2>
    <table>
    <tr>
      <th>Jaar</th><th>Aantal</th> 
    </tr><tr>
      <td>2014</td> <td class="played">%(year2014)s</td>
    </tr>
    </table>
"""

    # deel 2, maanden
    h_part2_d = u"""
    <h2>Maanden</h2>
    <table>
    <tr>
    <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th>
    <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th>
    </tr>
    <tr>
        <td class="maand">01</td>
        <td>%(month1)s</td> 
        <td class="maand">02</td> 
        <td>%(month2)s</td>
        <td class="maand">03</td> 
        <td>%(month3)s</td>
        
        <td class="maand">04</td> 
        <td>%(month4)s</td> 
        <td class="maand">05</td> 
        <td>%(month5)s</td> 
        <td class="maand">06</td> 
        <td>%(month6)s</td>
    </tr>
    <tr>
        <td class="maand">07</td> 
        <td>%(month7)s</td>  
        <td class="maand">08</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=8">%(month8)s</a> </td>  
        <td class="maand">09</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=9">%(month9)s</a> </td>

        <td class="maand">10</td> 
        <td>%(month10)s</td> 
        <td class="maand">11</td> 
        <td>%(month11)s</td> 
        <td class="maand">12</td> 
        <td>%(month12)s</td>
    </tr>
    </table>
"""

    # deel 3, dagen
    h_part3_d = u"""
    <h2>Dagen</h2>
    <table>
    <tr>
    <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> 
    <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> 
    </tr><tr>
        <td class="dag">01</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb1)s">%(day1)s</a> </td> 
        <td class="dag">02</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb2)s">%(day2)s</a> </td> 
        <td class="dag">03</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb3)s">%(day3)s</a> </td>
        <td class="dag">04</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb4)s">%(day4)s</a> </td>
        <td class="dag">05</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb5)s">%(day5)s</a> </td>
        <td class="dag">06</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb6)s">%(day6)s</a> </td>
    </tr><tr>
        <td class="dag">07</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb7)s">%(day7)s</a> </td>  
        <td class="dag">08</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb8)s">%(day8)s</a> </td>  
        <td class="dag">09</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb9)s">%(day9)s</a> </td>  
        <td class="dag">10</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb10)s">%(day10)s</a> </td>  
        <td class="dag">11</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb11)s">%(day11)s</a> </td>  
        <td class="dag">12</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb12)s">%(day12)s</a> </td>  
    </tr><tr>
        <td class="dag">13</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb13)s">%(day13)s</a> </td>  
        <td class="dag">14</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb14)s">%(day14)s</a> </td>  
        <td class="dag">15</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb15)s">%(day15)s</a> </td>  
        <td class="dag">16</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb16)s">%(day16)s</a> </td>  
        <td class="dag">17</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb17)s">%(day17)s</a> </td>  
        <td class="dag">18</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb18)s">%(day18)s</a> </td>  
    </tr><tr>
        <td class="dag">19</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb19)s">%(day19)s</a> </td>  
        <td class="dag">20</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb20)s">%(day20)s</a> </td>  
        <td class="dag">21</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb21)s">%(day21)s</a> </td>  
        <td class="dag">22</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb22)s">%(day22)s</a> </td>  
        <td class="dag">23</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb23)s">%(day23)s</a> </td>  
        <td class="dag">24</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb24)s">%(day24)s</a> </td>  
    </tr><tr>
        <td class="dag">25</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb25)s">%(day25)s</a> </td>  
        <td class="dag">26</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb26)s">%(day26)s</a> </td>  
        <td class="dag">27</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb27)s">%(day27)s</a> </td>  
        <td class="dag">28</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb28)s">%(day28)s</a> </td>  
        <td class="dag">29</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb29)s">%(day29)s</a> </td>  
        <td class="dag">30</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb30)s">%(day30)s</a> </td>  
        <td class="dag">31</td> <td class="played"> <a href="pagePlayedHistoryDetails?datum=%(dayb31)s">%(day31)s</a> </td>  
    </tr>
    </table>
"""

    # ontbrekende maanden toevoegen
    for tel in range(1, 13):
        key = u'month' + str(tel)
        if key not in monthsdict.keys():
            monthsdict[key] = ''
    # print 'monthsdict', monthsdict

    # ontbrekende dagen toevoegen
    for tel in range(1, 32):
        key = u'day' + str(tel)
        if key not in daysdict.keys():
            daysdict[key] = u''
        key = u'dayb' + str(tel)
        if key not in daysdict.keys():
            daysdict[key] = u''
    
    h_page = (h_part1_d % yearsdict)
    h_page = h_page + (h_part2_d % monthsdict)
    h_page = h_page + (h_part3_d % daysdict)
    h = h + html_page(h_page) + html_end()

    return h


def pagePlayedArtists():
    """Menu pagina naar aantal afgespeelde songs per periode en per artiest.
    """

    title = u'pagePlayedArtists'
    h = html_start(title) + main_navigation() + html_h1(u'Afspeeld per artiest, periode selectie') + \
    html_page(u"""
    <h2>Kies een periode</h2>
    <table>
        <tr>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=lastday">Laatste dag</a> <td>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=lasthalfyear">Laatste halfjaar</a> <td>
        </tr><tr>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=lastweek">Laatste week</a> <td>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=lastyear">Laatste jaar</a> <td>
        </tr><tr>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=last4weeks">Laatste 4 weken</a> <td>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=alltime">Alles</a> <td>
        </tr><tr>
            <td class="PlayedArtists"> <a href="pagePlayedArtistsPeriod?period=last3months">Laatste 3 maanden</a> <td>
        </tr>
        
    </table>
    """) + html_end()
    # print u'pagina', h    

    return h


def pagePlayedArtistsPeriod(period, records):
    """Aantal afgespeelde songs per artiest over een gekozen periode.
    """

    title = u'pagePlayedArtistsPeriod' 
    h_page = html_start(title) + main_navigation() + html_h1(u'Afgespeeld: ' + period)
    
    h = unicode(' ', 'utf-8', errors='replace')
    h = h + TABO + u"""
    <tr> 
        <td class="track">#</td> 
        <td class="artist">Artiest</td>
        <td class="played">Aantal</td> 
    </tr>
    """
    
    for record in records:
        h_td = unicode(' ', 'utf-8', errors='replace')
        h_td = h_td + TRO
        h_td = h_td + u"""<td class="track">%(volgnr)s</td>""" % {u'volgnr': record[u'volgnr']}
        
        # TODO, volgende 5 regels
        print 'artist', record['artist']
        # artist = unicode(record['artist'], 'utf-8', errors='replace')
        artist_link = record[u'artist'] # urllib.quote(record[u'artist'])
        artist = record['artist']
        # print 'artist_link', artist_link
        
        h_td = h_td + u"""<td class="artist">
            <a href="pagePlayedArtistsPeriodAlbums?period=%(period)s&artist_id=%(artist_id)s"> %(artist)s </a> </td>""" \
            % ({u'artist': artist, u'played': record[u'played'], \
            u'artist_id': record[u'artist_id'], u'period': period})
        h_td = h_td + u"""<td class="played">%(played)s</td>""" % {u'played': record[u'played']}
        
        link = hLink(u'aantal', u'pageShowSongs&period=%s&artist=%s' % (period, artist_link))
        # h_td = h_td + """href="pageShowSongs&period=&artist="aantal""" % (artist_link, period)
        
        h_td = h_td + TRC
        # h_td = unicode(h_td, 'utf-8', errors='replace')
        h = h + h_td

    h = h + TABC
    
    h_page = h_page + html_page(h) + html_end()

    return h_page  # + str(records)
    

def pagePlayedArtistsPeriodAlbums(period, artist_id, records):
    """Aantal afgespeelde songs van een artiest, per album over een gekozen periode.
    """

    title = u'pagePlayedArtistsPeriodAlbums'
    h = html_start(title) + main_navigation() + \
        html_h1(u"Afgespeeld: " + period + u", artiest: " + records[0]['artist'])
    
    h_page = TABO 
    h_page = h_page + u"""
    <tr>
        <th>Artiest</th>
        <th>Album</th> 
        <th>Aantal</th>
    </tr>
    """

    for record in records:
        h_td = TRO + \
            u"""<td class="artist">""" + record['artist'] + TDC + \
            u"""<td class="album">""" + linkpageAlbumTracks(record[u'album'], record[u'album_id']) + TDC + \
            u"""<td class="played">""" + str(record['played']) + TDC + TRC
        h_page = h_page + h_td

    h = h + TABC
    
    h = h + html_page(h_page) + html_end()
    # print h

    return h


def pageListAlbums_AlbumArtist(records):
    """Geef pagina terug met alle albums van een albumartiest. 
    """

    title = u'pageListAlbums_AlbumArtist'
    h = html_start(title) + main_navigation() + \
        html_h1(u'Albums van: %s' % records[0][u'albumartist'])

    # 2 parameters, link naar plaatje (folder_jpg), album naam (album)
    h_td = u"""
<td class="thumb">
    <a href="listAlbumTracks?album_id=%(album_id)s">
        <image class="thumb" src="%(folder_jpg)s"><br>
        <p class="thumb">%(album)s (%(year)s)</p>
    </a>
</td>
"""

    table = hTable()

    # doorloop alle records
    tel = 0
    for record in records:
        tel = tel + 1
    
        if tel == 1:
            table.add(TRO)
    
        table.add(h_td % record)
    
        if tel == 4:
            table.add(TRC)
            tel = 0

    if tel != 0:
        table.add(TRC)
    table.closeall()

    h = h + html_page(table.exp()) + html_end()
    return h


def listAlbumTracks(album_id, records):
    """HTML voor: toon alle songs van een album
    """

    # pagina title 
    title = u'listAlbumTracks'
    
    # pagina kop
    if len(records) > 0:
        album = records[0]['albumartist'] + " - " + records[0]['album']
        if len(album) > 51:
            album = album[0:45] + " . . ."
    else:
        album = "geen"
    h = html_start(title) + main_navigation() + html_h1(u'Album: %s') % album
    
    table = hTable()
    table.add(TRO + u"""
    <th>Playlist</th> <th>Play</th> <th>Track</th> <th>Titel</th> <th>Lengte</th> <th>Bitrate</th>
    """ + TRC)
    
    for record in records:
        # print str(record['tracknumber']), record['title']
        table.add(u'<tr class="ExtraHoog">') 
        table.add(TDO + u'<a href="playAlsoSong?song_id=' + str(record[u'song_id']) + u'">' \
                  + u'Add</a>' + TDC)
        
        table.add(TDO + u'<a href="playSong?song_id=' + str(record[u'song_id']) + u'">' \
                  + u' Play</a>' + TDC)
        
        table.add(TDO + str(record[u'tracknumber']) + TDC)
        
        title = record[u'title']
        # title = unicode(title, 'utf-8', errors='replace')
        # print 'title', type(title), title
        table.add(TDO + title + u"</a>" + TDC)
        
        table.add(TDO + str(record[u'length']) + TDC)
        table.add(TDO + str(record[u'bitrate']) + TDC)
        table.add(TDO + u'<a href="pageSong?song_id=' + str(record[u'song_id']) + '">')
        table.add(u"Infopage" + u'</a>' + TDC)
        table.add(TRC)
            
    h = h + html_page(table.exp()) + html_end()
    
    return h


def pageAfgespeeld():
    """Menu pagina voor afgespeeld
    """

    title = u'pageAfgespeeld'
    h = html_start(title) + main_navigation() + html_h1(u"Afgespeeld") 

    table = hTable()
    link = hLink(u"Afgespeeld per jaar / maand / dag", u"pagePlayedHistory")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Afgespeeld laatste tijd per artiest", u"pagePlayedArtists")
    table.td(link, u'beheer')
    table.tr()

    return h + html_page(table.exp()) + html_end()



def tableWithSongs(records):
    """Geef tabel terug met de records in <table> opmaak.
    Velden: info, volgnr, titel, artiest, album, jaar
    Vanaf 14 sept 2014, extra nodig: album_id, albumartist_id
    """

    # table header (th)
    h_tr_h = u"""
<tr>
    <th>Info</th>
    <th>#</th>
    <th>Titel (link voeg toe aan wachtrij)</th>
    <th>Artiest</th>
    <th>Album /
        Jaar /
        Rating 
    </th>
</tr>
"""

    # table data regel (td)
    h_td = u"""
<tr>
    <td class="info" rowspan="2">
        <a href="pageSong?song_id=%(song_id)s">Info</a>
    </td>
  
    <td class="track" rowspan="2">
        %(volgnr)s
    </td>
  
    <td class="title" rowspan="2">
        <a href="playAlsoSong?song_id=%(song_id)s">
        %(title)s
        </a>
    </td>

    <td class="artist" rowspan="2">
        <a href="pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s">
        %(artist)s
        </a>
    </td>

    <td class="album">
        <a href="listAlbumTracks?album_id=%(album_id)s">
        %(album)s
        </a>
    </td>
</tr>
<tr>
    <td colspan="1">
        %(year)s /
        %(rating)s  
    </td>
</tr>
"""

    table = hTable()

    if len(records) == 0:
        table.td(u"""<br>Geen gegevens gevonden die aan de selectie voldoen.""")
    else:
        table.add(h_tr_h)
        for record in records:
            # print 'record', record
            table.add(h_td % record)

    table.closeall()

    return table.exp()


def pagePlayedHistoryDetails(datum, records):
    """Toon details (songs), afgespeelde songs op een bepaalde datum.
    """

    title = u'pagePlayedHistoryDetails'
    h = unicode(' ', 'utf-8', errors="replace")
    toon_datum = datum[6:] + '-' + datum[4:6] + '-' + datum[:4]
    h = h + html_start('title') + main_navigation() + html_h1(u"Afgespeeld: %s" % toon_datum)
    
    h = h + html_page(tableWithSongs(records))
    
    h = h + html_end()

    return h


def pageMenuSearch():
    """Menu pagina voor zoeken.
    """

    title = 'pageMenuSearch'
    h = html_start(title) + main_navigation() + html_h1("Zoeken") 
    
    table = hTable()
    link = hLink(u"Vrij zoeken", u"pageSearch")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Zoeken met selecties", u"pageSearchWithSelections")
    table.td(link, u'beheer')
    table.tr()
    
    return h + html_page(table.exp()) + html_end()

# eof
