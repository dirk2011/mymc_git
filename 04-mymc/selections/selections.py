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
        """Database verbinding maken.
        @ivar _db: database  
        """
        self._db = MyDB() 


    @cherrypy.expose
    def index(self):
        """Hoofd ingang muteren selections. 
        Pagina geeft een lijst van bestaande selections.
        """

        query = """
            select     selection_id, selection, description, condition
            ,          to_char(adddate, 'yyyy-mm-dd') as adddate
            from       selections
            order by   selection 
        """
        records = self._db.dbGetData(query)

        h = selections_temp.pageSelectionsList(records)

        return h


    @cherrypy.expose
    def new(self):
        """Buttton new afhandelen, om nieuwe selections toe te voegen.
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
        records = self._db.dbGetData(query)

        h = selections_temp.pageSelection(records)
        
        return h


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save(self, txtCode="#", txtDescr="#", txtCond="#", txtId="#"):
        """Button saven afhandelen, een selection opslaan.
        """

        # probeer een update, deze lukt indien conditie al bestaat
        if len(txtId) > 1:
            query = """
                update selections set selection = '%s', description = '%s', condition = '%s'
                where selection_id = '%s'
            """ % (q(txtCode), q(txtDescr), q(txtCond), txtId)
            print "update query: ", query
            self._db.dbExecute(query)
        
        # probeer een insert, deze lukt indien conditie nog niet bestaat
        query = """
            insert into selections (selection, description, condition) 
            select '%s', '%s', '%s'
            where not exists (select 1 from selections where selection = '%s') 
        """ % (q(txtCode), q(txtDescr), q(txtCond), q(txtCode))
        self._db.dbExecute(query)

        return 


    @cherrypy.expose
    def delete(self, txtCode="#"):
        """Button delete afhandelen, een selection verwijderen. 
        """

        query = "delete from selections where selection = '%s'" % txtCode
        self._db.dbExecute(query)

        return
