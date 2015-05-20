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

import htable
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
    h.td(hButton(u'Queue', u'btnQueue', u'menuknop', u'/queuebeheer'))
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

<tr>
    <td colspan="2">
    <fieldset><legend>Songstekst</legend>
    <table>
    <tr><td>
    <form action="pageSongLyricSave">

    <textarea name="lyric" cols="60" rows="%(song_lyric_lines)s">
%(lyric)s</textarea>
    <br><br>
    <input type="submit" value="Ok">
    <input type="text" hidden name="song_id" value="%(song_id)s">
    
    </form>
    </td></tr>
    </table>
    </fieldset>
    </td>
</tr>

</td></tr></table>
""") + html_end()


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
        </tr><tr class="ExtraHoog">
            <td> Table parameters    </td><td> %(num_parameters)s </td>
        </tr><tr class="ExtraHoog">
            <td> Table songslyrics   </td><td> %(num_songslyrics)s </td>
        </tr><tr class="ExtraHoog">
            <td> Table tags          </td><td> %(num_tags)s (objecten met één of meerdere tags)</td>
        </tr><tr class="ExtraHoog">
            <td> Table tagslov       </td><td> %(num_tagslov)s (tags list of values)</td>
        </tr><tr class="ExtraHoog">
            <td> Table tags          </td><td> %(num_usedtags)s (aantal gebruikte tags in table 
                tags)</td>
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
      <!-- # 2015-05, volume stand 2 toegevoegd, voor slaap stand -->
	  <td class="SonosSpeakers"><a href="sonosSetVolume?speaker=%(ip_address)s&volume=2">2</td>
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
        <th class="SonosSpeakers">Volgnr</th>
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
    table.td("Pagina's in cache", u'beheer')
    table.tr()
    link = hLink(u"Clear cache, verwijder gegenereerde webpagina's.", u"pageClearCache")
    table.td(link, u'beheer')
    link = hLink(u"Toon pagina's in cache", u"pageShowCache")
    table.td(link, u'beheer')
    table.tr()

    table.td("Statistieken", u'beheer')
    table.tr()
    link = hLink(u"Ververs afgespeeld per jaar/maand/dag", u"pageRefreshPlayedHistory2")
    table.td(link, u'beheer')
    link = hLink(u"Controle", u"pageCheckPlayedHistory")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Ververs afgespeelde artiesten", u"pageRefreshPlayedArtists")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Ververs afgespeelde jaar/maand/artiesten/albums", u"pageRefreshPlayedAlbums")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Ververs afgespeelde jaar/maand/artiesten", u"pageRefreshPlayedAlbumsArtists")
    table.td(link, u'beheer')
    link = hLink(u"Controle", u"pageCheckPlayedAlbumsArtists")
    table.td(link, u'beheer')
    table.tr()

    table.td("Song id's vullen", u'beheer')
    table.tr()
    link = hLink(u"Vul album Id van nieuwe songs", u"pageDbSongsUpdateAlbumId")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Vul albumartist Id van nieuwe songs", u"pageDbSongsUpdateAlbumArtistId")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Vul artist Id van nieuwe songs", u"pageDbSongsUpdateArtistId")
    table.td(link, u'beheer')
    table.tr()
    
    table.td("Info", u'beheer')
    table.tr()
    link = hLink(u"Software versies", u"pageSoftwareVersions")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"About me / over mij", u"pageAboutMe")
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

    
def pagePlayedHistory(year, month, yearsdict, monthsdict, daysdict):
    """Toon webpagina met afspeel resultaten per jaar, maand, dag,
    met doorklik naar ander jaar en maand.
    """

    title = u'pagePlayedHistory'
    h = html_start(title) + main_navigation() + html_h1(u'Afgespeeld per periode')

    # totaal van allen jaren
    h_year_t = u"""
        <h2>Jaren, totaal: %(played)s</h2>
"""
    # totaal per jaar
    h_year_d = u"""
        <table>
            <tr>
                <td class="played">
                    %(year)s
                </td>  
            </tr><tr>
                <td class="played">
                    <a href="pagePlayedHistory?year=%(year)s"> %(played)s </a>
                </td>
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
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=1">%(month1)s</a> </td>  
        <td class="maand">02</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=2">%(month2)s</a> </td>  
        <td class="maand">03</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=3">%(month3)s</a> </td>  
        
        <td class="maand">04</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=4">%(month4)s</a> </td>  
        <td class="maand">05</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=5">%(month5)s</a> </td>  
        <td class="maand">06</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=6">%(month6)s</a> </td>  
    </tr>
    <tr>
        <td class="maand">07</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=7">%(month7)s</a> </td>  
        <td class="maand">08</td>
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=8">%(month8)s</a> </td>  
        <td class="maand">09</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=9">%(month9)s</a> </td>

        <td class="maand">10</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=10">%(month10)s</a> </td> 
        <td class="maand">11</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=11">%(month11)s</a> </td> 
        <td class="maand">12</td> 
        <td class="played"> <a href="pagePlayedHistory?year=%(year)s&month=12">%(month12)s</a> </td> 
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

    ### genereer html
    ## h2 heade, totaal alle jaren
    record = yearsdict[0]
    yearsdict = yearsdict[1:]
    h_page = h_year_t % record 

    ## de jaren
    h_jaren = hTable()
    for record in yearsdict:
        print "html record: ", record
        h_jaren.add(TDO)
        h_jaren.add(h_year_d % record)
        h_jaren.add(TDC)
    h_page = h_page + h_jaren.exp()

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
    """Html template voor: toon alle songs van een album
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

    # table header (th) 
    ht_th = """<tr>
        <th rowspan="2" class="info">Info</th> 
        <th rowspan="2" class="track">#</th> 
        <th             class="title"> Titel (link = voeg toe)</th> 
        <th rowspan="2" class="rating"> W </th>
        <th             class="artist">Album artiest</th>
        <th             class="firstlast"> Eerste keer </th>
        <th rowspan="2" class="played">T</th>
        <th rowspan="2" class="played">LQ</th>
        <th rowspan="2" class="played">LM</th>
        <th rowspan="2" class="played">LW</th>
    </tr>
    <tr>
        <th class="length"> Speeltijd </th>
        <th class="artist"> Artiest </th>
        <th class="firstlast"> Laatste keer </th>
    </tr>
    <tr>
        <td class="lijn" colspan="10"> </td>
    </tr>
    """
    
    # table data (td)
    ht_td = u"""<tr class="tr_track">
        <td rowspan="2" class="info">
            <a href="/pageSong?song_id=%(song_id)s">Info</a>
        </td>
        <td rowspan="2" class="track">
            %(volgnr)s
        </td>
        <td class="title">
            <a href="/playAlsoSong?song_id=%(song_id)s">
                %(title)s
            </a>
        </td>
        <td rowspan="2" class="rating"> %(rating)s
        <td class="artist">
            <a href="/pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s">
                %(albumartist)s
            </a>
        </td>
        <td class="firstlast">
                %(firstplayed)s
        </td>
        <td rowspan="2" class="played"> %(played)s </td>
        <td rowspan="2" class="played"> %(lq)s </td>
        <td rowspan="2" class="played"> %(lm)s </td>
        <td rowspan="2" class="played"> %(lw)s </td>
    </tr>
    <tr>
        <td class="length"> %(length)s - Lyric: %(lyric)s </td>
        <td class="artist"> %(artist)s </td>
        <td class="firstlast"> %(lastplayed)s </td>
    </tr>
    <tr>
        <td class="lijn" colspan="10"> </td>
    </tr>
    """

    # button naar tags van het album, 2015-04
    htags = """
    <form action="pageTagRefresh">
    <br>
    <input type="submit" value="Tags album">
    <input type="text" hidden name="album_id" value="%s">
    <br>
    </form>
    """ % album_id

    # doorloop alle records
    table = hTable()
    table.add(ht_th)    
    for record in records:
        table.add(ht_td % record)
            
    h = h + html_page(table.exp() + htags) + html_end()
    
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
    link = hLink(u"Afgespeeld per jaar/maand albumartiest", u"pagePlayedPeriodAlbumsArtists")
    table.td(link, u'beheer')
    table.tr()
    link = hLink(u"Afgespeelde 1000-tallen", u"pageTimeline")
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
    table.td(hButton(u'Vrij zoeken', u'btn1', u'menuknop2', u'pageSearch'))
    table.tr()
    table.td(hButton(u'Beheer selecties', u'btn3', u'menuknop2', u'/pageSelections'))
    table.tr()
    table.td(hButton(u'Zoeken met selecties', u'btn2', u'menuknop2', u'pageSearchWithSelections'))
    table.tr()
    table.td(hButton(u'Beheer super selecties', u'btn4', u'menuknop2', \
            u'/pageSearchWithSelections/manageSuperSelections'))
    table.tr()
    table.td(hButton(u'Albums en songteksten', u'btn5', u'menuknop2', u'/pageAlbumsWithLyrics'))
    table.tr()
    table.td(hButton(u'Beheer tags', u'btn6', u'menuknop2', u'/pageTagsBeheer/index'))
    table.tr()
    table.td(hButton(u'Zoeken met tags', u'btn7', u'menuknop2', u'/pageSearchWithTags'))
    table.tr()
    
    return h + html_page(table.exp()) + html_end()


def pageIndex():
    """Index (start) pagina van mymc.
    """
    
    page = u"""
    <img src="/static/images/music_017.jpg">
    """
    title = u'pageIndex'
    h_page = html_start(title) + main_navigation() + html_h1(u'MY Music Collection') + html_page(page) + html_end()
    
    return h_page


def pageSoftwareVersions(records):
    """Template pagina voor tonen versies gebruikte python software
    """

    title = 'pageSoftwareVersions'
    h = html_start(title) + main_navigation() + html_h1("Gebruikte python software versies")

    ht_page = """
    <table>
        <tr>
            <td class="software">Python versie: </td> 
            <td class="software">%(python)s</td>
        </tr></tr>
            <td class="software">Cherrypy versie: </td> 
            <td class="software">%(cherrypy)s</td>
        </tr></tr>
            <td class="software">Soco versie: </td> 
            <td class="software">%(soco)s</td>
        </tr>
    </table>
    """ % records

    h = h + html_page(ht_page) + html_end() 

    return h


def pageAboutMe(records):
    """Template pagina voor informatie over deze applicatie
    """

    title = 'pageAboutMe'
    h = html_start(title) + main_navigation() + html_h1("About me / over mij")

    ht_page = """
    <table>
        <tr>
            <td> %(info)s </td>
        </tr>
    </table>
    """ % records

    h = h + html_page(ht_page) + html_end() 

    return h


def pageRefreshPlayedAlbums():
    """Template pagina, verversen / aanvullen afgespeelde albums info, per jaar / maand.
    """

    title = u'pageRefreshPlayedAlbums'
    h = html_start(title) + main_navigation() + html_h1(title) + html_page(u"""

    <script>
        window.history.back();
    </script>

""") + html_end()

    return h


def pageRefreshPlayedAlbumsArtists():
    """Template pagina, verversen / aanvullen afgespeelde artiesten info, per jaar / maand.
    """

    title = u'pageRefreshPlayedAlbumsArtists'
    h = html_start(title) + main_navigation() + html_h1(title) + html_page(u"""

    <script>
        window.history.back();
    </script>

""") + html_end()

    return h


def pagePlayedPeriodAlbumsArtists(year, month, year_records, month_records, records):
    """ Template voor pagina played period albumsartists per jaar / maand
    """

    title = u'pagePlayedPeriodAlbumsArtists'
    h = html_start(title) + main_navigation() + html_h1("Afgespeeld per jaar/maand albumartiest " + \
                                                        str(year) + "/" + str(month))

    # template table jaren
    ht_jaren = """
    <h2>Jaren</h2>
    <table> <tr>
    %s    <!-- jaren -->
    </tr> </table>
    """

    # template jaren details
    ht_jaar = """
    <td>Jaar<br> <a href="pagePlayedPeriodAlbumsArtists?year=%(yr)s"> %(yr)s </a>
    </td>
    """
    
    # template table maanden
    ht_maanden = """
    <h2>Maanden</h2>
    <table>
    %s    <!-- header -->
    %s    <!-- maanden -->
    </table>
    """
    
    # template maanden header
    ht_maand_header = """
    <tr> <th>Maand</th> <th>Aantal</th> <th>Maand</th> <th>Aantal</th> <th>Maand</th> <th>Aantal</th>
    <th>Maand</th> <th>Aantal</th> <th>Maand</th> <th>Aantal</th> <th>Maand</th> <th>Aantal</th> </tr>
    """
    
    # template maanden details
    ht_maand = """
    <td> %(month)s </td> 
    <td> <a href="pagePlayedPeriodAlbumsArtists?year=%(yr)s&month=%(month)s"> %(played_songs)s </a> </td>
    """
    
    # template table albumartiesten
    ht_aa = """
    <h2>Albumartiesten</h2>
    <table>
    %s     <!-- artiesten -->
    </table>
    """
    
    # template detail albumartiesten
    ht_aa_detail = """
    <td>
        <table class="jmaa_table">
        <tr><td colspan="2" class="jmaa_artist">
            <a href="pagePlayedPeriodAlbums?year=%(yr)s&month=%(month)s&albumartist_id=%(albumartist_id)s">
            %(volgnr)s) %(albumartist)s </a> 
        </td></tr>
        <tr><td class="jmaa_label">Laatst:</td><td> %(played_last)s </td></tr>
        <tr><td class="jmaa_label">Eerst: </td><td> %(played_first)s </td></tr>
        <tr><td class="jmaa_label">Aantal: </td><td> %(played_songs)s </td></tr>
        </table>
    </td>
    """

    ## vul table jaren
    htab1 = Html()
    for record in year_records:
        htab1.add(ht_jaar % record)
    htab1 =  ht_jaren % htab1.exp()
    
    ## vul table maanden
    htab2 = Html()
    tel = 0
    for record in month_records:
        # als 0 begin nieuwe rij
        if tel == 0:
            htab2.add(TRO)
        tel += 1
        
        htab2.add(ht_maand % record)
        
        # als 6 sluit rij af
        if tel == 6:
            htab2.add(TRC)
            tel = 0
    htab2 = ht_maanden % (ht_maand_header, htab2.exp()) 
    
    ## vul table albumartiesten
    htab3 = Html()
    htab3.add(TRO)
    tel = 0
    for record in records:
        htab3.add(ht_aa_detail % record)

        # als <n> sluit rij af
        tel += 1
        if tel == 5:
            htab3.add(TRC + TRO)
            tel = 0
    htab3.add(TRC)
    htab3 = ht_aa % htab3.exp()
    
    h = h + html_page(htab1 + htab2 + htab3) + html_end()

    return h


def pagePlayedPeriodAlbums(year, month, albumartist, albumartist_id, records):
    """ Template voor pagina played period albums
    """

    title = u'pagePlayedPeriodAlbums'
    h = html_start(title) + main_navigation() + html_h1("Afgespeeld per jaar/maand albumartiest " + \
                                                        str(year) + "/" + str(month))

        
    # template table maanden
    ht_albums = """
    <h2> <a href="pageListAlbums_AlbumArtist?albumartist_id=%s">Artiest: %s </a> </h2>
    <table>
    %s    <!-- albums -->
    </table>
    """
    
    # template album details
    ht_album = """
    <td>
        <table class="jmaa_table">
        <tr><td colspan="2">
             <a href="listAlbumTracks?album_id=%(album_id)s"> 
                <img class="thumb" src="%(album_folder_jpg)s">
            </a>
        </td></tr>
        <tr><td colspan="2" class="">%(volgnr)s) %(album)s </td></tr>
        <tr><td class="jmaa_label">Laatst:</td><td> %(played_last)s </td></tr>
        <tr><td class="jmaa_label">Eerst: </td><td> %(played_first)s </td></tr>
        <tr><td class="jmaa_label">Aantal: </td><td> %(played_songs)s / %(album_songs)s </td></tr>
        </table>
    </td>
    """

    ## vul table albums
    htab1 = Html()
    htab1.add(TRO)
    tel = 0
    for record in records:
        htab1.add(ht_album % record)

        # als <n> sluit rij af
        tel += 1
        if tel == 5:
            htab1.add(TRC + TRO)
            tel = 0
    htab1.add(TRC)
    htab1 = ht_albums % (albumartist_id, albumartist, htab1.exp())
    
    h = h + html_page(htab1) + html_end()

    return h


def pageReturn():
    """Template pagina, doet maar één ding terug naar vorige pagina
    """

    title = u'pageReturn'
    h = html_start(title) + main_navigation() + html_h1(title) + html_page(u"""

    <script>
        window.history.back();
    </script>

""") + html_end()

    return h

def pageCheckPlayedAlbumsArtists(records1, records2, records3, records4, records5):
    """ Template voor pageCheckPlayedAlbumsArtists 
    """

    title = u'pageCheckPlayedAlbumsArtists'
    h = html_start(title) + main_navigation() + html_h1("Steekproeven: afgespeeld per jaar/maand albumartiest")

    ht_1 = """
        <tr><td>Controle 1</td></tr>
        <tr><td></td> <td>Aantal afgespeeld: </td> <td> %(played_songs)s </td></tr>
    """
    
    ht_2 = """
        <tr><td>Controle 2</td></tr>
        <tr><td></td> <td>Eerste jaar: </td> <td> %(yr)s </td></tr>
        <tr><td></td> <td>Eerste maand: </td> <td> %(month)s </td></tr>
        <tr><td></td> <td>Eerste dag: </td> <td> %(played_first)s </td></tr>
    """
    
    ht_3 = """
        <tr><td>Controle 3</td></tr>
        <tr><td></td> <td>Laatste jaar: </td> <td> %(yr)s </td></tr>
        <tr><td></td> <td>Laatste maand: </td> <td> %(month)s </td></tr>
        <tr><td></td> <td>Laatste dag: </td> <td> %(played_last)s </td></tr>
    """

    ht_4 = """
        <tr><td>Controle 4</td></tr>
        <tr><td></td> <td>Unieke eerste dagen: </td> <td> %(played_first)s </td></tr>
    """

    ht_5 = """
        <tr><td>Controle 5</td></tr>
        <tr><td></td> <td>Unieke albumartiesten: </td> <td> %(albumartist_count)s </td></tr>
    """

    ht_table = """
    <table>
        %s    <!-- 1 -->
        %s    <!-- 2 -->
        %s    <!-- 3 -->
        %s    <!-- 4 -->
        %s    <!-- 5 -->
    </table>
    """

    ht_1 = ht_1 % records1[0]
    ht_2 = ht_2 % records2[0]
    ht_3 = ht_3 % records3[0]
    ht_4 = ht_4 % records4[0]
    ht_5 = ht_5 % records5[0]
    ht_table = ht_table % (ht_1, ht_2, ht_3, ht_4, ht_5)

    h = h + html_page(ht_table + html_end())

    return h


def pageCheckPlayedHistory(records):
    """Template pagina voor pageCheckPlayedHistory 
    """

    title = u'pageCheckPlayedHistory'
    h = html_start(title) + main_navigation() + html_h1("Eenvoudige visuele controle played_history")

    # header
    ht_h = """
        <tr>
            <th class="volgnr">Volgnr</th>
            <th class="telling">Telling</th>
            <th class="soort">Soort</th>
            <th class="aantal">Aantal</th>
        </tr>
    """
    
    # td regel
    ht_d = """
        <tr>
            <td class="volgnr">%(volgnr)s</td>
            <td class="telling">%(telling)s</td>
            <td class="soort">%(soort)s</td>
            <td class="aantal">%(aantal)s</td>
        </tr>
    """
    
    ht_t = """
        <table>
            %s <!-- header -->
            %s <!-- rijen -->
        </table>
    """

    table = Html()
    for record in records:
        table.add(ht_d % record)

    h = h + html_page(ht_t % (ht_h, table.exp()) + html_end())

    return h


def pageTimeline(records):
    """Template voor tonen afgespeelde 1000-tallen.
    """
    
    title = u'pageTimeline'
    h = html_start(title) + main_navigation() + html_h1("Afgespeelde 1000-tallen")

    ht_table = """
    <table>
        %s <!-- header -->
        %s <!-- data   -->
    </table>
    """
    
    ht_th = """
        <tr>
            <th class="volgnr">Volgnr</th>
            <th class="datum">Datum</th>
            <th class="afgespeeld">Afgespeeld</th>
            <th class="dagen">Dagen</th>
        </tr>
    """
    
    ht_td = """
        <tr>
            <td class="volgnr">%(sort)s</td>
            <td class="datum">%(playdate)s</td>
            <td class="afgespeeld">%(played)s</td>
            <td class="dagen">%(days)s</td>
        </tr>
    """

    tab = Html()
    for record in records:
        if record['days'] is not None:
            record['days'] = int(record['days'])
        else:
            record['days'] = ""
        tab.add(ht_td % record)
    tab = tab.exp()
        
    h = h + html_page(ht_table % (ht_th, tab) + html_end())
    
    return h


def pageAlbumsWithLyrics(records):
    """Template pagina voor tonen albums met songteksten
    """

    title = u'pageAlbumsWithLyrics'
    h = html_start(title) + main_navigation() + html_h1("Albums met songteksten")

    # table template
    ht_table = """
    <table>
        %s <!-- header -->
        %s <!-- data   -->
    </table>
    """
    
    # table header
    ht_th = u"""
        <tr>
            <th class="artist"> Albumartiest </th>
            <th class="album"> Album </th>
            <th class="firstlast"> Songtekst toegevoegd </th>
            <th class="aantal"> Song- teksten </th>
            <th class="aantal"> Titels </th>
            <th class="firstlast"> Laatst afgespeeld </th>
        </tr>
    """

    ht_td = """
        <tr>
            <td class="artist">%(albumartist)s</td>
            <td class="album">
                <a href="/listAlbumTracks?album_id=%(album_id)s">
                    %(album)s
                </a>
            </td>
            <td class="firstlast">%(lyric_added)s</td>
            <td class="aantal">%(lyrics)s</td>
            <td class="aantal">%(songs)s</td>
            <td class="firstlast">%(lastplayed)s</td>
        </tr>
    """

    tab = Html()
    totaal = 0
    for record in records:
        totaal = totaal + record['lyrics']
        tab.add(ht_td % record)
    tab = tab.exp()

    h = h + html_page(ht_table % (ht_th, tab) +\
                      u"<br><b>Totaal aantal songteksten: %s </b><br>" % totaal +\
                      html_end())

    return h


####################################################################################################
def pageTagRefresh(mObject, mObjectId, objectDesc, allTags, usedTags):
    """Template pagina voor wijzigen tags van een object
    toegevoegd: 2015-04
    """

    title = u'pageTagRefresh'
    h = html_start(title) + main_navigation() + html_h1("Tags toevoegen en wijzigen")

    # javascript voor afhandelen buttons
    h_js = u"""
<script type="text/javascript">
$(document).ready(function() {
    // AT = all tags, op geklikt, zet used tags button aan
    $("[id*=btnAT]").click(function() {
        var btn = this.id ;
        var txtTag = btn.substr(5) ;
        var usedTag = "btnUT" + txtTag ;
        $('#' + usedTag).show() ;
    });

    // UT = used tags, er is op een used tag geklikt maak deze hidden
    $("[id*=btnUT]").click(function() {
        $(this).hide();
    });

    // button save (opslaan) afhandelen
    $("#btnSave").click(function() {
        txtTags = ""
        // vraag visibility op van alle btnUT* buttons
        $("[id*=btnUT]").each(function() {
            // var btn = this.id ;
            // var txtTag = btn.substr(5) ;
            // var usedTag = "btnUT" + txtTag ;
            // $('#' + usedTag).show() ;
            var isVisible = $(this).is(':visible');
            if (isVisible) {
                // waarde van button aan gekozen tags toevoegen
                txtTags = txtTags + this.value + "," ;
            }
        });
        // alert (txtTags) ;

        $.ajax({
            url: "tagssave",
            type: "POST",
            data: {mObject:   $("#mObject").val()
                  ,mObjectId: $("#mObjectId").val()
                  ,txtTags:   txtTags },
            success: function(response) {
                /* window.location = "index"; */
                /* alert(btn); */
                /* $("#test").html(response); */
                }
        });
        // terug naar vorige pagina
        parent.history.back();
    });

    // terug (back) button
    $("#btnBack").click(function() {
        parent.history.back();
    //     return false;
    });
});
</script>
    """

    # pagina bestaat uit 5 blokken
    ht_table = u"""
    <table> <tr><td>
        %s <!-- javascript -->
        %s <!-- object -->
        %s <!-- alle tags -->
        %s <!-- gebruikte tags -->
        %s <!-- actie knoppen -->
    </td></tr> </table>
    """

    # pagina deel 1, object omschrijving
    objectDesc = objectDesc.decode('utf-8')
    h1 = u"""
    <fieldset><legend>Object</legend>
        <table><tr>
        <td>%s</td>
        <td align="right">
        <input type="text" id="mObject"   value="%s" hidden readonly tabindex="-1">
        <input type="text" id="mObjectId" value="%s" hidden readonly tabindex="-1">
        </td>
        </tr></table>
    </fieldset>
    """ % (objectDesc, mObject, mObjectId)

    # pagina deel 2, alle tags
    h2 = """
    <fieldset><legend>Beschikbare tags</legend>
    %s
    </fieldset>
    """
    h2at = ""
    for tag in allTags:
        h2at = h2at + '<input class="zmsbtnSel" type="button" value="%s" id="btnAT%s"> ' \
                % (tag, tag)
    h2 = h2 % h2at

    # pagina deel 3, gebruikte tags
    h3 = """
    <fieldset><legend>Gebruikte tags</legend>
    %s
    </fieldset>
    """
    h3ut = ""
    for tag in allTags:
        if tag in usedTags:
            hidden = ""
        else:
            hidden = "hidden "
        h3ut = h3ut + '<input class="zmsbtnSel" type="button" %s value="%s" id="btnUT%s"> ' \
                % (hidden, tag, tag)
    h3 = h3 % h3ut

    # pagina deel 4, acties
    h4 = """
    <fieldset><legend>Acties</legend>
        <input type="button" value="Opslaan" id="btnSave">
        <input type="button" value="Terug"   id="btnBack">
    </fieldset>
    """

    h = h + html_page(ht_table % (h_js, h1, h2, h3, h4) + \
        html_end())

    return h


####################################################################################################
def pageSearchWithTags(allTags):
    """Template pagina voor zoeken met tags
    toegevoegd: 2015-04
    """

    title = u'pageSearchWithTags'
    h = html_start(title) + main_navigation() + html_h1("Zoeken met tags")

    # style
    h_style = """
    <style>
.tagsveld {
    margin: 4px;
}
</style>
    """

    # javascript voor afhandelen buttons
    h_js = """
<script type="text/javascript">
$(document).ready(function() {
    // AT = all tags, op geklikt, zet used tags button aan
    $("[id*=btnAT]").click(function() {
        var btn = this.id ;
        var txtTag = btn.substr(5) ;
        var usedTag = "btnUT" + txtTag ;
        $('#' + usedTag).show() ;
    });

    // UT = used tags, er is op een used tag geklikt maak deze hidden
    $("[id*=btnUT]").click(function() {
        $(this).hide();
    });

    // button save (opslaan) afhandelen
    $("#btnSearch").click(function() {
        txtTags = ""
        // vraag visibility op van alle btnUT* buttons
        $("[id*=btnUT]").each(function() {
            // var btn = this.id ;
            // var txtTag = btn.substr(5) ;
            // var usedTag = "btnUT" + txtTag ;
            // $('#' + usedTag).show() ;
            var isVisible = $(this).is(':visible');
            if (isVisible) {
                // waarde van button aan gekozen tags toevoegen
                txtTag = this.id ;
                txtTag = txtTag.substr(5) ;
                txtTags = txtTags + txtTag + "," ;
            }
        });
        // alert (txtTags) ;

        window.location = "pageFindWithTags?txtTags=" + txtTags ;
        //alternatief: window.location.replace("pageFindWithTags?txtTags=" + product_id);
    });
});
</script>
    """

    # pagina bestaat uit een aantal blokken
    ht_table = """
    <table> <tr><td>
        %s <!-- style -->
        %s <!-- javascript -->
        %s <!-- alle tags -->
        %s <!-- gebruikte tags -->
        %s <!-- actie knoppen -->
    </td></tr> </table>
    """

    # pagina deel 1, alle tags die voorkomen, hiermee kan gezocht worden
    h1 = """
    <fieldset><legend>Tags waarmee gezocht kan worden</legend>
    %s
    </fieldset>
    """
    h1at = ""
    for tag in allTags:
        h1at = h1at + '<input class="tagsveld" type="button" value="%s" id="btnAT%s"> ' \
                % (tag['tag'] + " (%s)" % tag['aantal'], tag['tag'])
    h1 = h1 % h1at

    # pagina deel 2, gebruikte tags
    h2 = """
    <fieldset><legend>Zoek met volgende tags</legend>
    %s
    </fieldset>
    """
    h2ut = ""
    for tag in allTags:
        h2ut = h2ut + '<input class="tagsveld" hidden type="button" value="%s" id="btnUT%s"> ' \
                % (tag['tag'] + " (%s)" % tag['aantal'], tag['tag'])
    h2 = h2 % h2ut

    # pagina deel 4, acties
    h3 = """
    <fieldset><legend>Acties</legend>
        <input type="button" value="Zoeken" id="btnSearch">
    </fieldset>
    """

    h = h + html_page(ht_table % (h_style, h_js, h1, h2, h3) + \
        html_end())

    return h


####################################################################################################
def pageFindWithTags(records, txtTags):
    """template pagina voor weergeven gezocht albums mbv tags
    toegevoegd: 2015-04
    """

    title = u'pageFindWithTags'
    h = html_start(title) + main_navigation() + html_h1("Gevonden albums")

    # java script
    ht_js = """
<script type="text/javascript">
$(document).ready(function() {
    // terug (back) button
    $("#btnBack").click(function() {
        parent.history.back();
    //     return false;
    });
});
</script>
    """

    # table template
    ht_table = """
    <table>
        %s <!-- header -->
        %s <!-- data   -->
    </table>
    """
    
    # header voor de table
    txtTags = txtTags.strip(',')
    ht_tags = "<h2>Gezocht op: %s </h2>" % txtTags

    # table header
    ht_th = u"""
        <tr>
            <th class="artist"> Albumartiest </th>
            <th class="album"> Album </th>
            <th class="tags"> Tags </th>
        </tr>
    """

    ht_td = """
        <tr>
            <td class="artist">%(albumartist)s</td>
            <td class="album">
                <a href="/listAlbumTracks?album_id=%(album_id)s">
                    %(album)s
                </a>
            </td>
            <td class="tags"> %(tags)s </td>
        </tr>
    """

    tab = Html()
    teller = 0
    for record in records:
        tab.add(ht_td % record)
        teller += 1
    tab = tab.exp()

    ht_tel = """
        <br>Aantal: %s<br>
        <br>
        <input type="button" value="Terug"   id="btnBack">
    """ % teller

    h = h + html_page(ht_js + ht_tags + ht_table % (ht_th, tab) + ht_tel + html_end())
    # print "mymc_html.pageFindWithTags", h

    return h


# eof

