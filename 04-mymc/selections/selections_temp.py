# -*- coding: utf-8 -*-

"""Module selections_temp.

Pagina tempates voor om table selections te bewerken.

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


def pageSelection(records):
    """Pagina template voor muteren van één selection.
    """

    title = "pageSelections"
    h = html_start(title) + main_navigation() + html_h1("Selectie")
    
    hRecord = """
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
        $("#info").html("niets aan de hand");
        if ( $("#txtCode").val().length < 1 || $("#txtCond").val().length < 1 ) {  
            if ( $("#txtCond").val().length < 1 ) {
                $("#info").html("Conditie invullen svp");
            }
            if ($("#txtCode").val().length < 1) {
                $("#info").html("Code invullen svp");
            }
        } else {
            $("#info").html("Selectie wordt opgeslagen . . .");
            $.ajax({
                url: "save",
                type: "POST",
                data: {txtCode: $("#txtCode").val(), txtDescr: $("#txtDescr").val(),
                    txtCond: $("#txtCond").val()},
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
        $("#info").html("Selectie wordt verwijderd . . .");

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


<fieldset id="invoer-gebied"><legend id="invoer-label">Muteren selectie</legend>
<form id="testform">
<table>
  <tr>
    <td>
      Selectie
    </td><td>
      <input type="text" id="txtCode" size="30" maxlength="30" value="%(selection)s">
      <input type="hidden" type="text" id="txtId" size="10" value="%(selection_id)s">
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
      Conditie
    </td><td>
      <input type="text" id="txtCond" size="100" maxlength="100" value="%(condition)s"><br>
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
        print 'records: ', records

        h = h + html_page(hRecord % record)
        
    h = h + html_end()

    return h


def pageSelectionsList(records):
    """Pagina template voor een overzicht van bestaande selections.
    """

    title ="pageSelectionsList"
    h = html_start(title) + main_navigation() + html_h1("Selecties")

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
        <th>Selectie</th>
        <th>Toelichting</th> 
        <th>Conditie</th>
        <th>Toegevoegd</th>
    </tr>
    """

    h_td = """
    <tr>
        <td>%(tel)s</td>
        <td> <a href="pageSelection?id=%(selection_id)s"> %(selection)s </a> </td>
        <td>%(description)s</td>
        <td>%(condition)s</td>
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
