# -*- coding: utf-8 -*-

"""Module selections.

Bevat ......................

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
import searchwithselections_temp
reload(searchwithselections_temp)

from dbfunc import MyDB
from dbfunc import q


class pageSearchWithSelections(object):
    """Zoeken met selections
        @since: 2014-09
        @version: 1
    """

    def __init__(self):
        """Database verbinding wordt hier gemaakt.
        @ivar _db: database  
        """
        self._db = MyDB() 

    @cherrypy.expose
    def index(self):
        """
        """

        # query1, selections laden
        query1 = """
            select    *
            from      selections
            order by  selection
        """
        records1 = self._db.dbGetData(query1)
        
        # query2, conditions/selections laden
        query2 = """
            select    swc.condition, swc.selection_id, s.selection
            from      swc    -- selection with conditions
            join      selections as s
            on        swc.selection_id = s.selection_id
            where     swc.condition != 0
            order by  swc.condition, swc.selection_id ;
        """
        records2 = self._db.dbGetData(query2)

        h = searchwithselections_temp.pageSearchWithSelections(records1, records2)
                
        return h

    @cherrypy.expose
    def saveselectie(self, selection_id):
        """Button selectie afhandelen, er is een nieuwe selectie gekozen
        """

        # ontvangen wordt bijvoorbeeld: btnSel54 
        selection_id = selection_id[6:]
        
        # controleer of selectie al opgeslagen is
        query = """
            select count(*) as aantal
            from swc
            where condition = 0 and selection_id = %s
        """ % selection_id
        records = self._db.dbGetData(query)
        print 'records: ', records

        if len(records) > 0:
            aantal = records[0]['aantal']
            if aantal < 1:
                # selectie komt nog niet voor, opslaan
                query = """
                    insert into swc (condition, selection_id) values (0, %s)
                """ % selection_id
                self._db.dbExecute(query)
        
        return

