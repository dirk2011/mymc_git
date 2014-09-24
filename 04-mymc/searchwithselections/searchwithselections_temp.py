# -*- coding: utf-8 -*-

"""Module selections_temp.

Pagina tempates voor SearchWithSelections.

"""


__author__  = 'dp'
__date__    = '2014-09'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


from htable import hTable
from hTable import Html
from hTable import hLink, hButton
from hTable import TDO, TDC, TRO, TRC, TABO, TABC

from mymc_html import html_start
from mymc_html import main_navigation
from mymc_html import html_page
from mymc_html import html_h1
from mymc_html import html_end


def pageSearchWithSelections(records1, records2):
    """Template voor index pagina, searchwithselections. 
    """

    title ="pageSearchWithSelections"
    h = html_start(title) + main_navigation() + html_h1("Zoeken met selections")

    h_js = """
<script type="text/javascript">
$(document).ready(function() {
    $("[id*=btnSel]").click(function() {
        /* haal id op van ingedrukte button */
        var btn = this.id;
        $.ajax({
        url: "saveselectie",
        type: "POST",
        data: {selection_id: btn },
        success: function(response) {
            /* window.location = "index";    /* terug naar de lijst */
            /* alert(btn); */
            /* $("#test").html(response); */
            }
        });
    });

    $("[id*=btnCond]").click(function() {
        /* haal id op van ingedrukte button */
        var btn = this.id;
        $.ajax({
        url: "savecondition",
        type: "POST",
        data: {condition: btn },
        success: function(response) {
            window.location = "index";
            /* alert(btn); */
            /* $("#test").html(response); */
            }
        });
    });

    $("[id*=btnFil]").click(function() {
        /* haal id op van ingedrukte button */
        var btn = this.id;
        $.ajax({
        url: "deleteselectie",
        type: "POST",
        data: {selection_id: btn },
        success: function(response) {
            window.location = "index";
            /* alert(btn); */
            /* $("#test").html(response); */
            }
        });
    });

    $("#btnDeleteAll").click(function() {
        /* haal id op van ingedrukte button */
        var btn = this.id;
        $.ajax({
            url: "deleteall",
            type: "POST",
            data: {id: btn },
            success: function(response) {
            window.location = "index";
            /* alert(btn); */
            /* $("#test").html(response); */
            }
        });
    });

    $("#btnRun").click(function() {
        window.location = "runselection";
    });

    $("[id*=btnxCond]").click(function() {
        /* haal id op van ingedrukte button */
        var btn = this.id;
        alert(btn);
    });

});

</script>

    """

    h_style = """
    <style>
/* zms = zoeken met seletions */

.zmsbtnSel {
    margin: 5px;
}
.zmsbtnCon {
    margin: 5px;
}
.zmsbtnAct {
    margin: 5px;
}

/* table1 bevat alles */
.zmstab1 {
    width: 850px;
}
/* table2 bevat conditie toevoeg knoppen */
.zmstab2 {
    width: 100%;
}

.zmstd {
    text-align: left;
      vertical-align: text-top;
      width: 25%;
}

.zmscentre {
    text-align: center;
}

/* fieldset conditions */
.zmsfscond {
     min-height: 100px;     
}

/* gebieden die ververst moeten worden met gekozen condities
#zmcCond1 t/m 4
*/

</style>
    """

    ## tr1, template, gebied voor laden selecties    
    ht_tr1 = """
    <tr>
    <td colspan="4">
      <fieldset><legend>Selecties</legend>
      %s <!-- hier selecties laden -->
    </fieldset>
    </td>
</tr>
    """
    
    ## td1, template, selecties
    ht_td1 = """
        <button class="zmsbtnSel" type="button" id="btnSel%(selection_id)s">%(selection)s</button>
    """

    ## selections verwerken, voor weergave in html table
    tab1 = Html()
    for record in records1:
        tab1.add(ht_td1 % record)
    tab1 = ht_tr1 % tab1.exp()


    ### laden conditie verwerk buttons
    tab2 = """
    <tr>
        <td colspan="4">
        <fieldset><legend>Voeg toe aan conditie</legend>
            <table class="zmstab2"><tr>
            <td class="zmscentre"><button class="zmsbtnCon" type="button" id="btnCond1">Conditie 1</button>
            <td class="zmscentre"><button class="zmsbtnCon" type="button" id="btnCond2">Conditie 2</button>
            <td class="zmscentre"><button class="zmsbtnCon" type="button" id="btnCond3">Conditie 3</button>
            <td class="zmscentre"><button class="zmsbtnCon" type="button" id="btnCond4">Conditie 4</button>
            </tr></table>
        </fieldset>
        </td>
    </tr>
    """


    ### laden condities met selecties
    # structuur (tr)
    ht3_tr = """    
    <tr>
    <td class="zmstd">
    <fieldset class="zmsfscond"><legend>Conditie 1</legend>
    <div id="zmcCond1">
        %s <!-- conditie 1 selecties -->
      </div>
      </fieldset>
    </td>
    <td class="zmstd">
    <fieldset class="zmsfscond"><legend>Conditie 2</legend>
    <div id="zmcCond2">
        %s <! -- conditie 2 selecties -->
      </div>
      </fieldset>
    </td>
    <td class="zmstd">
    <fieldset class="zmsfscond"><legend>Conditie 3</legend>
    <div id="zmcCond3">
        %s <! -- conditie 3 selecties -->
      </div>
      </fieldset>
    </td>
    <td class="zmstd">
    <fieldset class="zmsfscond"><legend>Conditie 4</legend>
    <div id="zmcCond4">
        %s <! -- conditie 4 selecties -->
      </div>
      </fieldset>
    </td>
</tr>
 """
 
    # td3, template
    ht3_td = """
        <button class="zmsbtnSel" type="button" id="btnFil%s">%s</button>
    """
    
    # conditie 1 opbouwen
    cond1 = ""
    for record in records2:
        if record['condition'] == 1:
            cond1 = cond1 + ht3_td % ('1' + str(record['selection_id']), record['selection'])
        
    # conditie 2 opbouwen
    cond2 = ""
    for record in records2:
        if record['condition'] == 2:
            cond2 = cond2 + ht3_td % ('2' + str(record['selection_id']), record['selection'])

    # conditie 3 opbouwen
    cond3 = ""
    for record in records2:
        if record['condition'] == 3:
            cond3 = cond3 + ht3_td % ('3' + str(record['selection_id']), record['selection'])

    # conditie 4 opbouwen
    cond4 = ""
    for record in records2:
        if record['condition'] == 4:
            cond4 = cond4 + ht3_td % ('4' + str(record['selection_id']), record['selection'])
    
    tab3 = ht3_tr % (cond1, cond2, cond3, cond4)


    ## de hoofd table
    table = """
    <table class="zmstab1">
    %s <!-- table 1: selections -->
    
    %s <!-- table 2: conditie verwerk buttons -->
    
    %s <!-- table 3: condities met selecties --> 
    
    <tr>
        <td colspan="4">
            <fieldset><legend>Acties</legend>
            <button class="zmsbtnAct" type="button" id="btnRun">Toepassen</button>
            <button class="zmsbtnAct" type="button" id="btnDeleteAll">Wis condities</button>
            </fieldset>
        </td>
    </tr>

    </table>
    """
    
    table = table % (tab1, tab2, tab3)

    return h + html_page(table) + h_style + h_js + html_end()


def pageRunselection(records):
    """Template voor paginga "zoek songs via de selecties".
    """

    title ="pageRunselection"
    h = html_start(title) + main_navigation() + html_h1("Zoek resultaat")

    ht_th = """<tr>
        <th class="info">Info</th> 
        <th class="track">#</th> 
        <th class="title">
            Titel
            <br>(voeg aan afspeellijst toe)
        </th> 
        <th class="artist">Artiest</th>
        <th class="album">Album
            <br>Rating/Jaar/Gespeeld/Laatst
        </th>
    </tr>
    """

    ht_td = """<tr>
        <td class="info">
            <a href="/pageSong?song_id=%(song_id)s">Info</a>
        </td>
        
        <td class="track">
            %(volgnr)s
        </td>
        
        <td class="title">
            <a href="/playAlsoSong?song_id=%(song_id)s">
                %(title)s
            </a>
        </td>
        
        <td class="artist">
            <a href="/pageListAlbums_AlbumArtist?albumartist_id=%(albumartist_id)s">
                %(albumartist)s
            </a>
            <br>%(artist)s
        </td>
        
        <td class="album">
            <a href="/listAlbumTracks?album_id=%(album_id)s">
                %(album)s
            </a>
            <br>%(rating)s / %(year)s / %(played)s / %(lastplayed)s
        </td>
    </tr>"""

    table = Html()
    table.add(TABO)
    if len(records) == 0:
        # zijn er wel gegevens gevonden
        table.add(TRO + TDO + "Geen gegevens gevonden :(" + TDC + TRC)
    else:
        table.add(ht_th)
        # laat gevonden gegevens zien
        for record in records:
            # print "record: ", record
            table.add(ht_td % record)
    table.add(TABC)

    return h + html_page(table.exp()) + html_end()

# eof
