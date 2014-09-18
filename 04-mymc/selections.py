# -*- coding: utf-8 -*-

"""Module selections.

Bevat class om table selections te muteren.

"""

__author__  = 'dp'
__date__    = '2014-09'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


import cherrypy             # cherrypy de webinterface
import mymc_html            # web pagina's
reload(mymc_html)
from dbfunc import MyDB
from dbfunc import q


class pageSelections(object):
    """Muteren van de table selections.
    """

    def __init__(self):
        """Initialisatie
        """
        pass

    @cherrypy.expose
    def index(self):
        """De webpagina voor het muteren
        """

        h = mymc_html.pageSelections()

        return h
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save(self, txtCode="#", txtDescr="#", txtCond="#"):

        db = MyDB()
        query = "delete from selections where selection = '%s'" % txtCode
        db.dbExecute(query)
        query = """insert into selections (selection, description, condition) 
            values ('%s', '%s', '%s') """ % (txtCode, txtDescr, txtCond)
        db.dbExecute(query)

        return """alert("1: %s, 2: %s, 3: %s);""" % (txtCode, txtDescr, txtCond)
        pass


    @cherrypy.expose
    def delete(self, txtCode="#"):

        db = MyDB()
        query = "delete from selections where selection = '%s'" % txtCode
        db.dbExecute(query)
        
        return """alert(verwijderd"""

    @cherrypy.expose
    def test(self):
        
        return "<html>doe ie het ?</html>"
