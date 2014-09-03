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

class hTable():
    def __init__(self, options=""):
        """Aanmaken hTable object."""
        
        if len(options) == 0:
            self.html = "<table>"
        else:
            self.html = """<table %s>""" % options

        # level = status: table, trh, th of td
        self.level = "table"


    def exp(self):
        """Exporteer html code."""
        
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
        
        if self.level == "td":
            self.add("</td> ")
            self.level = "tr"
        elif self.level == "trh":
            self.add("</tr>")
            self.level = "table"
        elif self.level == "tr":
            self.add("</tr>")
            self.level = "table"
        elif self.level == "table":
            self.add("</table>")
            self.level = ""


    def tr(self, classs=""):
        """Begin tr niveau."""
        
        if len(classs) > 1:
            tag = """<tr class="%s">""" % classs
        else:
            tag = """<tr>"""

        if self.level == "table":
            self.add(tag)
        elif self.level == "trh":
            self.add("</tr>" + tag)
        elif self.level == "td":
            self.add("</td>" + "</tr>" + tag)
        elif self.level == "tr":
            return
        else:
            return
        self.level = "tr"


    def th(self, data="", classs=""):
        """Begin en einde van th (table header)."""
        
        data = str(data)
        if len(classs) > 1:
            tag = """<th class="%s">""" % classs
        else:
            tag = """<th>"""
        
        if self.level == "table":
            self.add(tag)
        elif self.level == "tr":
            self.add(tag)
        elif self.level == "td":
            return
        self.level = "trh"
        self.add("""%s</th>""" % data)


    def td(self, data="#", classs=""):
        """Begin van een td (table detail)."""
        
        data = str(data)
        if len(classs) > 1:
            tag = """<td class="%s">""" % classs
        else:
            tag = """<td>"""
        
        if self.level == "td":
            self.add("</td>" + tag)
        elif self.level == "tr":
            self.add(tag)
        elif self.level == "trh":
            self.add("</tr><tr>" + tag)
        elif self.level == "table":
            self.add("<tr>" + tag)
        else:
            return
        self.level = "td"
        self.add(data)


    def tda(self, data="#"):
        """Voeg data toe aan td (table detail)."""
        
        data = str(data)
        if self.level == "td":
            self.add(data)
        else:
            self.td(data)


if __name__ == "__main__":
    """Bedoeld voor testen. """
    
    html = hTable()
    html.th("header kolom 1")
    html.td("data kolom 1")
    html.closeall()
    html.exp()
