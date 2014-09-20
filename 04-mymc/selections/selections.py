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
# import HTMLParser

import mymc_html            # web pagina's
reload(mymc_html)
import selections_temp
reload(selections_temp)
from dbfunc import MyDB
from dbfunc import q


class pageSelections(object):
    """Muteren van de table selections.
        @since: 2014-09
        @version: 1
    """

    def __init__(self):
        """Initialisatie
        """
        self._db = MyDB() 

    @cherrypy.expose
    def index(self):
        """De webpagina voor het muteren
        """

        query = """
            select     selection_id, selection, description, condition
            ,          to_char(adddate, 'yyyy-mm-dd') as adddate
            from       selections
            order by   selection 
        """
        # self._db = MyDB()
        records = self._db.dbGetData(query)

        h = selections_temp.pageSelectionsList(records)

        return h


    @cherrypy.expose
    def new(self):
        """New buttton afhandelen, voor nieuwe selections toe te voegen.
        """
        
        # leeg record aanmaken
        record = {'selection': "", 'description': "", 'condition': "", 'selection_id': ""}
        records = [record]
        
        h = selections_temp.pageSelection(records)
        
        return h

    @cherrypy.expose
    def pageSelection(self, id):
        """Pagina voor het muteren van één selectie.
        """

        query = """
            select     selection_id, selection, description, condition
            ,          to_char(adddate, 'yyyy-mm-dd') as adddate
            from       selections
            where      selection_id = %s
            order by   selection 
        """ % id
        # db = MyDB()
        records = self._db.dbGetData(query)

        h = selections_temp.pageSelection(records)
        
        return h


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save(self, txtCode="#", txtDescr="#", txtCond="#"):
        """Save button afhandelen, een selection opslaan.
        """

        # db = MyDB()
        query = "delete from selections where selection = '%s'" % txtCode
        self._db.dbExecute(query)
        query = """insert into selections (selection, description, condition) 
            values ('%s', '%s', '%s') """ % (q(txtCode), q(txtDescr), q(txtCond))
        self._db.dbExecute(query)

        # return """alert("1: %s, 2: %s, 3: %s);""" % (q(txtCode), q(txtDescr), q(txtCond))
        return 


    @cherrypy.expose
    def delete(self, txtCode="#"):
        """Delete button afhandelen, een selection verwijderen.
        """

        # db = MyDB()
        query = "delete from selections where selection = '%s'" % txtCode
        self._db.dbExecute(query)

        return """alert(verwijderd"""
