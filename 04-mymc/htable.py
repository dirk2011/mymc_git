# -*- coding: utf-8 -*-

"""htable.py met class hTable

Met deze class kan eenvoudig een html table aangemaakt worden.

Gebruik: import hTable from htable

html = hTable()
html.th("header kolom 1")
html.td("data kolom 1")
html.closeall()
html.exp()

"""

__author__  = 'dp'
__date__    = '2014-09-07'
__version__ = '1'


# pylint: disable=C0103, C0301


TDO = u"<td>"           # <td>
TDC = u"</td>"          # </td>
TRO = u"<tr>"           # <tr>
TRC = u"""</tr>
"""                     # </tr>
TABO = u"<table>"       # <table>
TABC = u"</table>"      # </table>


class hTable():
    """Class voor aanmaken van een table in html.
    """

    def __init__(self, options=""):
        """Aanmaken hTable object."""

        if len(options) == 0:
            self.html = u"""<table>
"""
        else:
            self.html = u"""<table %s>""" % options

        # level = status: table, trh, th of td
        self.level = u"table"


    def exp(self):
        """Exporteer html code."""

        self.closeall()
        # print self.html
        return self.html


    def add(self, data=""):
        """Interne methode, tekst aan html string toevoegen """

        self.html = self.html + data


    def closeall(self):
        """Sluit tabel af."""
        self.close()
        self.close()
        self.close()


    def close(self):
        """Sluit een niveau af.
        Het is niet nodig deze zelf aan te roepen, gebruik op het einde: closeall.
        """

        if self.level == u"td":
            self.add(u"</td> ")
            self.level = u"tr"
        elif self.level == u"trh":
            self.add(u"</tr>")
            self.level = u"table"
        elif self.level == u"tr":
            self.add(u"""
</tr>""")
            self.level = u"table"
        elif self.level == u"table":
            self.add(u"""</table>""")
            self.level = u""


    def tr(self, classs=""):
        """Begin tr niveau."""

        if len(classs) > 1:
            tag = u"""
<tr class="%s">""" % classs
        else:
            tag = u"""
<tr>"""

        if self.level == u"table":
            self.add(tag)
        elif self.level == u"trh":
            self.add(u"""</tr>""" + tag)
        elif self.level == u"td":
            self.add(u"</td>" + u"""</tr>""" + tag)
        elif self.level == u"tr":
            return
        else:
            return
        self.level = u"tr"
        # self.add('tr level: ' + self.level)


    def th(self, data="", classs=""):
        """Begin en einde van th (table header)."""

        data = str(data)
        if len(classs) > 1:
            tag = u"""<th class="%s">""" % classs
        else:
            tag = u"""<th>"""

        if self.level == u"table":
            self.add(tag)
        elif self.level == u"tr":
            self.add(tag)
        elif self.level == u"td":
            return
        self.level = u"trh"
        self.add(u"""%s</th>""" % data)


    def td(self, data="#", classs=""):
        """Begin van een td (table detail)."""

        # data = str(data)
        if len(classs) > 1:
            tag = u"""<td class="%s">""" % classs
        else:
            tag = u"""<td>"""

        if self.level == u"td":
            self.add("</td>" + tag)
        elif self.level == u"tr":
            self.add(tag)
        elif self.level == u"trh":
            self.add(u"""
</tr>
<tr>""" + tag)
        elif self.level == u"table":
            self.add(u"<tr>" + tag)
        else:
            return
        self.level = u"td"
        # self.add('td level: ' + self.level)
        self.add(data)


    def tda(self, data="#"):
        """Voeg data toe aan td (table detail)."""

        data = str(data)
        if self.level == u"td":
            self.add(data)
        else:
            self.td(data)


class Html():
    """Eenvoudige class om text aan elkaar te plakken.
    In plaats van steeds bijvoorbeeld: html = html + "<tr>" """

    def __init__(self):
        """Maak object aan."""
        self.html = ""

    def add(self, html):
        """Voeg text toe. """
        self.html = self.html + html

    def exp(self):
        """Vraag waarde op."""
        return self.html


def hLink(tekst, url):
    return u"""<a href="%s">%s</a>""" % (url, tekst)


if __name__ == "__main__":
    # Bedoeld voor testen.

    html = hTable()
    html.td(u"header kolom 1")
    html.tr()
    html.td(u"data kolom 1")
    html.tr()
    html.td(u'einde')
    html.closeall()
    print html.exp()
