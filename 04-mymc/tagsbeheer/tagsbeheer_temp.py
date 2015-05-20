# -*- coding: utf-8 -*-

"""Module tags template.

Pagina tempates om tags te bewerken

"""


__author__  = 'dp'
__date__    = '2015-04'


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


################################################################################
def pageTag(records):
    """Pagina template voor muteren van één tag
    """

    title = u"pageTag"
    h = html_start(title) + main_navigation() + html_h1(u"Eén tag beheren")
    
    hRecord = u"""
<style>
.knop {
  xtext-transform: uppercase;
  width: 10em;
  height: 2em;
}

#invoer-gebied {
  display: inline;
  background-color: #b0c4de;
  border-style: solid;
  border-width: 1px;
  border-color: black;
}

#invoer-label {
  background-color: #b0c4de;
  padding: 0.25em;
  border-style: solid;
  border-width: 1px;
}
</style>

<script type="text/javascript">
$(document).ready(function() {
    if ( $("#txtId").val().length < 1 ) {
        $("#btnDelete").hide();
    }

    $("#btnStore").click(function() {
        $("#info").html(" ");    /* meldingen gebied leegmaken */
        if ( $("#txtCode").val().length < 1 ) {  
            if ( $("#txtCond").val().length < 1 ) {
                $("#info").html("Conditie invullen svp");
            }
            if ($("#txtCode").val().length < 1) {
                $("#info").html("Code invullen svp");
            }
        } else {
            $("#info").html("Tag wordt opgeslagen . . .");
            $.ajax({
                url: "save",
                type: "POST",
                data: {txtCode: $("#txtCode").val(), txtDescr: $("#txtDescr").val(),
                    txtId: $("#txtId").val() },
                success: function(response) {
                    window.location = "index";    /* terug naar de lijst */
                    /* alert(response); */
                    /* $("#test").html(response); */
                    }
            });
        }    
        /* alert("I am an alert box!"); */
    });

    $("#btnDelete").click(function() {
        $.ajax({
            url: "delete",
            type: "POST",
            data: {txtCode: $("#txtCode").val()},
            success: function(response) {
                window.location = "index";
                /* alert(response); */
                /* $("#test").html(response); */
            }
        });
        $("#info").html("Tag wordt verwijderd . . .");

    });

    $("#btnLijst").click(function() {
        window.location = "index";
    });

    $("#btnCancel").click(function() {
        var a = $( "#testform" ).serialize() ; 
        alert(a);
        $.post( "save", $( "#testform" ).serialize() );
    });

});
</script>


<fieldset id="invoer-gebied"><legend id="invoer-label">Muteren tag</legend>
<form id="testform">
<table>
  <tr>
    <td>
     Tag 
    </td><td>
      <input type="text" id="txtCode" size="30" maxlength="30" value="%(tag)s">
      <input type="text" id="txtId" size="10" value="%(tag_id)s" readonly tabindex="-1">
    </td>
   </tr> 

   <tr>
    <td>
      Toelichting 
    </td><td>
      <input type="text" id="txtDescr" size="50" maxlength="100" value="%(description)s"><br>
    </td>
  </tr>
  
  <tr>
    <td>
    </td><td>
      <button type="button" class="knop" id="btnStore">Opslaan</button>
      <button type="button" class="knop" id="btnDelete">Verwijderen</button>
      <button type="button" class="knop" id="btnLijst">Lijst</button>
      <br>
      <p id="info"><!-- meldingen --></p>
     </td>
  </tr>
</table>
</form>
</fieldset>
"""

    if len(records) == 1:
        record = records[0]
        # record['condition'] = cgi.escape(record['condition'])
        print 'tagsbeheer_temp.pageTag, records: ', records

        h = h + html_page(hRecord % record)
        
    h = h + html_end()

    return h


################################################################################
def pageTagsList(records):
    """Pagina template, lijst alle tags, table tagslov
    """

    title ="pageTagsList"
    h = html_start(title) + main_navigation() + html_h1("Tags beheren")

    h_js = """
<script type="text/javascript">
$(document).ready(function() {
    $("#btnNew").click(function() {
        window.location = "new";
    });

});
</script>

    """
    
    h_th = """
    <tr>
        <th>#</th>
        <th>Tag</th>
        <th>Toelichting</th> 
        <th>Toegevoegd</th>
    </tr>
    """

    h_td = """
    <tr>
        <td>%(tel)s</td>
        <td> <a href="pageTag?id=%(tag_id)s"> %(tag)s </a> </td>
        <td>%(description)s</td>
        <td>%(adddate)s</td>
    </tr>
    """

    table = hTable()
    table.add(h_th)
    tel = 0
    for record in records:
        tel = tel + 1
        record['tel'] = tel
        table.add(h_td % record)

    return h + html_page("""<form>
        <button type="button"  id="btnNew">Toevoegen</button>
        </form>""" + table.exp()) + h_js + html_end()

# eof

