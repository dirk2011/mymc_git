# -*- coding: utf-8 -*-

"""Deze module hoort bij module mymc.

Deze module bevat strings en functies om webpagina's
te genereren. Hiervoor wordt gebruik gemaakt van
de python module pycheerry.

# TODO: alle variabelen omzetten naar functies
"""

t = """
<html>
hi %(naam)s
</html>
"""


def main_navigation():
    """Geef de kop terug voor webpagina's.
    In de kop staan links naar pagina's binnen de site.
    """

    return """
<link rel="stylesheet" type="text/css" href="/static/css/style.css">

<table>
  <tr>
    <td class="nav">
      <a href="index">Home</a>
    </td><td class="nav">
      <a href="pageInfoMc">Info Mc</a>
    </td><td class="nav">
      <a href="pageListAlbumArtists">Album artiesten</a>
    </td><td class="nav">
      <a href="pageSearch">Zoeken</a>
    </td><td class="nav">
      <a href="sonos_playmenu">Queue</a>
    </td><td class="nav">
      <a href="pageSonosSpeakers">Volume</a>
    </td><td class="nav">
      <a href="pagePlayedHistory">Play history</a>
    </td><td class="nav">
      <a href="pagePlayedArtists">Artist history</a>
    </td><td class="nav">
      <a href="pageClearCache">Clear Cache</a>
    </td>
  </tr>
</table>
"""

def pageSong():
    """Geef webpagina terug, met veel gegevens over een song.
    
    Input voor de mymc module is song_id.
    Terug door deze functione, de html pagina.
    """

    return """
<html>
<head><title>pageSong</title></head>
<body>""" + main_navigation() + \
"""


<h1>Song page</h1>

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
	</td>
	</tr><tr><td>
	  Title
	  </td><td>
	  %(title)s
	</td></tr><tr><td>

	  Artist
	</td><td>
	  %(artist)s
	</tr></tr><tr><td>

	  Length
	</td><td>
	  %(length)s
	</tr></tr><tr><td>

	  Album
	</td><td>
	  %(album)s
	</td></tr><tr><td>

	  Tracknumber
	</td><td>
	  %(tracknumber)s
	</td></tr><tr><td>

	  Albumartist
	</td><td>
	  %(albumartist)s
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
      </table>
      </fieldset>
    </td>
    
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
	  <input type="radio" name="rating" value="0" checked>0
	  <input type="radio" name="rating" value="1">1
	  <input type="radio" name="rating" value="2">2
	  <input type="radio" name="rating" value="3">3
	  <input type="radio" name="rating" value="4">4
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
</body>
</html>
"""


def sonos_playmenu():
    """Geef webpagina terug om afspeellijst (queue) te beheren.
    
    De queue kan afgespeeld en leeggemaakt worden. Tevens zijn er knoppen 
    voor previous, next, stop en pause.
    Oude naam: sonos_menu.
    """

    return """
<html>
  """ + main_navigation() + """
  <h1> sonos player commands and info </h1>

  <table>
    <tr>
      <td>
      <form action="sonos_previous">
      <input type="submit" value="Previous">
      </form>
      </td>

      <td>
      <form action="sonos_pause">
      <input type="submit" value="Pause">
      </form>
      </td>

      <td>
      <form action="sonos_play">
      <input type="submit" value="Play">
      </form>
      </td>
      
      <td>
      <form action="sonos_next">
      <input type="submit" value="Next">
      </form>
      </td>
      
      <td>
      <form action="sonos_clear_queue">
      <input type="submit" value="Clear queue">
      </form>
      </td>

      <td>
      <form action="sonos_play_from_queue">
      <input type="submit" value="Play queue">
      </form>
      </td>
    </tr>
  </table>

</html>
"""


def sonos_next():
    """Dummy pagina voor de next button.
    """
    
    return """
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
    
    return """
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
    
    return """
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
    
    return """
    <html>
    sonos_pause</br>

    <script>
	window.history.back();
    </script>

    </html>
"""


sonos_clear_queue = """
    <html>
    sonos_clear_queue</br>

    <script>
	window.history.back();
    </script>

    </html>
"""


sonos_play_from_queue = """
    <html>
    sonos_play_from_queue</br>

    <script>
	window.history.back();
    </script>

    </html>
"""


pageSongSave = """
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

    h_page_o = """
<html> 
""" + main_navigation() + """

<style type="text/css">
    td {
    padding: 20 20px 0 0;
    margin: 0;
    border: 0;
    }
</style>

<h1>Album artiesten</h1>

<table>
"""

    h_page_c="""
</table>

</html>
"""

    # table row, open
    h_tr_o = "<tr>"
    
    # table row, close
    h_tr_c = "</tr>"
    
    # table data
    h_td = """
    <td >
      
    </td><td>
      <a href="pageListAlbums_AlbumArtist?albumartist=%(albumartist_link)s">%(albumartist)s</a><br>
      %(volgnr)s / %(num_albums)s / %(num_songs)s
    </td>"""

    # begin van de pagina
    h = h_page_o

    # doorloop alle records
    tel = 0
    for record in records:
        # print 'record', record
        tel = tel + 1
	
        if tel == 1:
            h = h + h_tr_o
	
        h = h + (h_td % record)
	
        if tel == 4:
            h = h + h_tr_c
            tel = 0

    if tel <> 0:
        h = h + h_tr_c

    h = h + h_page_c
    
    return h


def testPageListAlbumArtists():
    """Functie voor het testen van pageListAlbumArtists() met dummy data.
    """
    
    record1 = {'volgnr': 1, 'albumartist': 'ABBA  ', 'num_songs': 63, 'num_albums': 5}
    record2 = {'volgnr': 1, 'albumartist': 'B ABBA', 'num_songs': 63, 'num_albums': 5}
    record3 = {'volgnr': 1, 'albumartist': 'C ABBA', 'num_songs': 63, 'num_albums': 5}
    record4 = {'volgnr': 1, 'albumartist': 'D ABBA', 'num_songs': 63, 'num_albums': 5}
    record5 = {'volgnr': 1, 'albumartist': 'E ABBA', 'num_songs': 63, 'num_albums': 5}
    records = [ record1, record2, record3, record4, record5 ]

    h = pageListAlbumArtists(records)
    print h

    return h


def pageListAlbums_AlbumArtist(records):
    """Geef pagina terug met alle albums van een albumartiest. 
    
    """
    # pagina begin, heeft parameter nodig: albumartist
    h_page_o = """
<html>

<style type="text/css">
    td {
    padding: 20 20px 0 0;
    margin: 0;
    border: 0;
    width: 195
    }
    img.thumb {
    width: 150px;
    heigth: 150px;
    }
    p.thumb {
    text-align: center;
    } 
</style>

""" + main_navigation() + """

<h1>Albumartiest: %(albumartist)s</h1>

<table>
"""

    h_tr_o = "<tr>"
    
    h_tr_c = "</tr>"

    # 2 parameters, link naar plaatje (folder_jpg), album naam (album)
    h_td = """
    <td align="center">
      <a href="listAlbumTracks?album=%(album_link)s">
	<image class="thumb" src="%(folder_jpg)s"><br>
	<p class="thumb">%(album)s (%(year)s)</p>
      </a>
    </td>
"""

    h_page_c = """
</table>

</html>
"""

    # begin van de pagina
    h = (h_page_o % records[0])

    # doorloop alle records
    tel = 0
    for record in records:
        # print 'record', record
        tel = tel + 1
	
        if tel == 1:
            h = h + h_tr_o
	
        h = h + (h_td % record)
	
        if tel == 4:
            h = h + h_tr_c
            tel = 0

    if tel <> 0:
        h = h + h_tr_c

    h = h + h_page_c

    return h

    
def testPageListAlbums_AlbumArtist():
    """Functie voor het testen van functie: pageListAlbums_AlbumArtist, met dummy data.
    """
    record1 = {'albumartist': 'Bee Gees', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record2 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record3 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record4 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    record5 = {'albumartist': 'ABBA', 'folder_jpg': 'folder.jpg', 'album': 'Arrival'}
    records = [ record1, record2, record3, record4, record5 ]

    h = pageListAlbums_AlbumArtist(records)
    # print h

    return h


# TODO pageInfoMc nog omzetten naar een functie
pageInfoMc = """
<html>
<head><title>pageInfoMc</title></head>

<style type="text/css">
    td {
    padding: 20 20px 0 0;
    margin: 0;
    border: 0;
    }
</style>

<body>

""" + main_navigation() + \
"""
<h1>Info over mijn muziekcollectie (mc)</h1>

<table>
  <tr><td> Table songs </td><td> %(num_song)s </td></tr>

  <tr><td>
    <a href="pageListAlbumArtists">Album artiesten</a>
  </td><td> %(num_albumartist)s </td></tr>

  <tr><td> Albums 	    </td><td> %(num_album)s </td></tr>
  <tr><td> Artiesten 	    </td><td> %(num_artist)s </td></tr>
  <tr><td> Table played    </td><td> %(num_played)s </td></tr>
  <tr><td> Table songsinfo </td><td> %(num_songsinfo)s (songs met een rating) </td></tr>
  <tr><td> Table queue     </td><td> %(num_queue)s (songs in afspeel queue) </td></tr>

</table>

</body>
</html>
"""


def pageSonosSpeakers(records):
    """Geef web pagina terug, om volume van de speakers te beheren.
    
    Tevens geeft dit inzicht in alle sonos componenten.
    """

    h_page_o = """
<html>
""" + main_navigation() + """

<style type="text/css">
    td {
    padding: 0 20px 0 0;
    margin: 0;
    border: 0;
    }
</style>

<h1>Sonos boxen</h1>

<table border="1">
<tr><th>Naam</th><th>Aan/Uit</th><th>Volume</th> <th>Zet volume</th><th>Component</th><th>Adres</th>
    <th>Coordinator</th>
</tr>
"""

    h_tr_o = "<tr>"
    
    h_tr_c = "</tr>"

    h_td = """
    <td>%(zone_name)s</td>
    <td>%(mute)s</td>
    <td>%(volume)s</td>
    <td>
      <table>
	<tr>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=0">0</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=10">10</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=15">15</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=20">20</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=25">25</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=30">30</td>

	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=40">40</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=50">50</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=60">60</td>
	  <td><a href="sonosSetVolume?speaker=%(ip_address)s&volume=70">70</td>
	</tr>
      </table>
    </td>

    <td>%(volgnr)s</td>
    <td>%(ip_address)s</td>
    <td>%(is_coordinator)s</td>
<!--    <td>%(is_speaker)s</td>
    <td>%(loudness)s</td>
    <td>%(treble)s</td>
    <td>%(bass)s</td>
    <td>%(status_light)s</td> -->

    """

    h_page_c = """
  </tr>
</table>

<p>Pagina laden duurt even, omdat bij iedere box gegevens worden opgehaald.</p>
<p>Ververs de pagina om actuele volume gegevens te zien.</p>
</html>
"""

    # begin van de pagina
    h = h_page_o

    # doorloop alle records
    tel = 0
    for record in records:
        # print 'record', record
        h = h + h_tr_o
	
        hd = (h_td % record)
        h = h + hd
	
        h = h + h_tr_c

    h = h + h_page_c
    print len(h)

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

    return """
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
    """Index (start) pagina van mc applicatie.
    """
    
    return """
    <html><head><title>Index</title></head>
    """ + main_navigation() + """       
    <body>
<br>
 /     \_/ ___\ <br>
|  Y Y  \  \___ <br>
|__|_|  /\___  ><br>
      \/     \/<br>
<br>      
    </body>
    </html>
    """


def pageSearch():
  
    return """
<html>
<head><title>Song search</title>
</head>
""" + main_navigation() + """
<h1>Songs zoeken</h1>

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

</html>
    """


def pageSearchResult(records):

    h_page_o = """
<html>
<head><title>Search result</title>
</head>
<body>
""" + main_navigation() + """
<h1>Zoek resultaat</h1>
<table>"""

    h_tr_h = """
<tr>
  <th>Info</th>
  <th>#</th>
  <th>Title (link is add to queue)</th>
  <th>Artist</th>
  <th>Album</th>

  <th>Year</th>
  <th>Last</th>
  <th>Played</th>
</tr>
"""

    h_tr_o = "<tr>"
    
    h_tr_c = "</tr>"

    h_td = """
<tr>
  <td class="info">
    <a href="pageSong?song_id=%(song_id)s">Info</a>
  </td>
  <td class="track">%(volgnr)s</td>
  <td class="title">
      <a href="playAlsoSong?song_id=%(song_id)s">
      %(title)s
      </a>
  </td>

  <td class="artist">
      <a href="pageListAlbums_AlbumArtist?albumartist=%(albumartist_link)s">
      %(artist)s
      </a>
  </td>
  <td class="album">
      <a href="listAlbumTracks?album=%(album_link)s">
      %(album)s
      </a>
  </td>
  <td class="year">
    %(year)s
  </td>
  <td class="last">
    %(last)s
  </td>
  <td class="played">
    %(played)s
  </td>
</tr>
"""

    h_page_c = """
</table>
</html>
"""

    h = h_page_o

    if len(records) == 0:
        h = h + """<br>Geen gegevens gevonden die aan de selectie voldoen.<br>
            Probeer het opnieuw."""
    else:
        h = h + h_tr_h
        for record in records:
            h =  h + (h_td % record)

    h = h + h_page_c

    return h


def pageClearCache(records):
    """Pagina om te tonen voor clear cache, toont verwijderde pagina's.
    """

    h_page_o =  """
    <html>
    <head><title>
    </title></head>
    <body>""" + main_navigation() + """
    <h1>Clear Cache</h1>
    <table>
    """

    h_tr_o = "<tr>"
    
    h_tr_c = "</tr>"

    h_td = """<td>%(regel)s</td>
    """
    
    h_page_c = """
    </table>
    </body>
    </html>
    """

    h = h_page_o

    if len(records) > 0:
        h = h + h_tr_o + """<td>De volgende pagina's zijn verwijderd.</td>""" + h_tr_c
        for record in records:
            h = h + h_tr_o
            h = h + (h_td % {'regel': record})
            h = h + h_tr_c
    else:
        h = h + """Er zijn geen pagina's in cache gevonden. """

    h = h + h_page_c

    return h


def pagePartSongRating(song_id, rating):
    """Stukje html etc, voor rating van songs, om in te voegen in andere pagina's,
       nodig: song_id, en huidige rating.
    """

    h_page = """
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
    record['song_id'] = song_id
    record['checked0'] = "checked" if rating == 0 else ""
    record['checked1'] = "checked" if rating == 1 else ""
    record['checked2'] = "checked" if rating == 2 else ""
    record['checked3'] = "checked" if rating == 3 else ""
    record['checked4'] = "checked" if rating == 4 else ""
    record['checked5'] = "checked" if rating == 5 else ""

    h = (h_page % record)

    return h

def testPagePartSongRating():
    """ Testen pagePartSongRating
    """
    
    song_id = 999
    rating = 5
    h = pagePartSongRating(song_id, rating)

    return h


def pagePlayedHistory(yearsdict, monthsdict, daysdict):
    """Toon webpagina met afspeel resultaten per jaar, maand, dag
    """

    h_page_o = """
<html>
<head><title>
</title></head>
<body>
""" + main_navigation() + """
<h1>Play history per period</h1>
"""

    h_part1_d = """
    <h2>Years</h2>
    <table>
    <tr>
      <th>Jaar</th><th>Aantal</th> 
    </tr><tr>
      <td>2014</td> <td>%(year2014)s</td>
    </tr>
    </table>
"""

    # deel 2, maanden
    h_part2_d = """
    <h2>Months</h2>
    <table>
    <tr>
	<th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th>
	<th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th> <th>Maand</th><th>Aantal</th>
    </tr><tr>
        <td>01</td> <td>%(month1)s</td> <td>02</td> <td>%(month2)s</td> <td>03</td> <td>%(month3)s</td>
        <td>04</td> <td>%(month4)s</td> <td>05</td> <td>%(month5)s</td> <td>06</td> <td>%(month6)s</td>
    </tr><tr>
        <td>07</td> <td>%(month7)s</td>  <td>08</td> <td>%(month8)s</td>  <td>09</td> <td>%(month9)s</td>
        <td>10</td> <td>%(month10)s</td> <td>11</td> <td>%(month11)s</td> <td>12</td> <td>%(month12)s</td>
    </tr>
    </table>
"""

    # deel 3, dagen
    h_part3_d = """
    <h2>Days</h2>
    <table>
    <tr>
	<th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> 
	<th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> <th>Dag</th><th>Aantal</th> 
    </tr><tr>
        <td>01</td> <td>%(day1)s</td> <td>02</td> <td>%(day2)s</td> <td>03</td> <td>%(day3)s</td>
        <td>04</td> <td>%(day4)s</td> <td>05</td> <td>%(day5)s</td> <td>06</td> <td>%(day6)s</td>
    </tr><tr>
        <td>07</td> <td>%(day7)s</td> <td>08</td> <td>%(day8)s</td> <td>09</td> <td>%(day9)s</td>
        <td>10</td> <td>%(day10)s</td> <td>11</td> <td>%(day11)s</td> <td>12</td> <td>%(day12)s</td>
    </tr><tr>
        <td>13</td> <td>%(day13)s</td> <td>14</td> <td>%(day14)s</td> <td>15</td> <td>%(day15)s</td>
        <td>16</td> <td>%(day16)s</td> <td>17</td> <td>%(day17)s</td> <td>18</td> <td>%(day18)s</td>
    </tr><tr>
        <td>19</td> <td>%(day19)s</td> <td>20</td> <td>%(day20)s</td> <td>21</td> <td>%(day21)s</td>
        <td>22</td> <td>%(day22)s</td> <td>23</td> <td>%(day23)s</td> <td>24</td> <td>%(day24)s</td>
    </tr><tr>
        <td>25</td> <td>%(day25)s</td> <td>26</td> <td>%(day26)s</td> <td>27</td> <td>%(day27)s</td>
        <td>28</td> <td>%(day28)s</td> <td>29</td> <td>%(day29)s</td> <td>30</td> <td>%(day30)s</td> <td>31</td> <td>%(day31)s</td>
    </tr>
    </table>
"""


    h_page_c = """
</body>
</html>"""

    h = h_page_o

    # ontbrekende maanden toevoegen
    for tel in range(1, 13):
        key = 'month' + str(tel)
        if key not in monthsdict.keys():
            monthsdict[key] = ''
    print 'monthsdict', monthsdict

    # ontbrekende dagen toevoegen
    for tel in range(1, 32):
        key = 'day' + str(tel)
        if key not in daysdict.keys():
            daysdict[key] = ''
    
    h = h + (h_part1_d % yearsdict)
    h = h + (h_part2_d % monthsdict)
    h = h + (h_part3_d % daysdict)
    h = h + h_page_c

    return h

def pagePlayedArtists():

    h_page = """
    <html><head><title>Afspeel gegevens per artiest, periode selectie
    </title></head>
    <body>""" + main_navigation() + """
    <h1>Afspeel gegevens per artiest</h1>
    <br>
    <h2>Kies een periode</h2>
    <table>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=lastday">Laatste dag</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=lastweek">Laatste week</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=last4weeks">Laatste 4 weken</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=last3months">Laatste 3 maanden</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=lasthalfyear">Laatste halfjaar</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=lastyear">Laatste jaar</a> <td></tr>
        <tr><td> <a href="pagePlayedArtistsPeriod?period=alltime">Alles</a> <td></tr>
    </table>

    </body>
    </html>
    """    

    return h_page


def pagePlayedArtistsPeriod(period, records):

    h_page_o = """
    <html><head><title>Afspeelgegevens, per artiest, """ + period + """
    </title></head>
    <body>""" + main_navigation() + """
    <h1>Overzicht afgespeeld: """ + period + """</h1>
    <table>"""

    h_page_c = """</table>
    </body>
    </html>"""

    h_tr_o = "<tr>"
    h_tr_c = "</tr>"

    h = unicode(' ', 'utf-8', errors='replace')
    h = h_page_o + h
    
    for record in records:
        h_td =  h_tr_o + """<td>%s</td> <td>%s</td> <td>%s</td>""" % \
            (record['volgnr'], record['artist'], record['played']) + h_tr_c
        h_td = unicode(h_td, 'utf-8', errors='replace')
        h = h + h_td

    return h # + str(records)
    
    
# einde

