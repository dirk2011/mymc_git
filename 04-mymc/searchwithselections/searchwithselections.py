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
        print 'query: ', query
        records = self._db.dbGetData(query)
        # print 'records: ', records

        if len(records) > 0:
            aantal = records[0]['aantal']
            if aantal < 1:
                # selectie komt nog niet voor, opslaan
                query = """
                    insert into swc (condition, selection_id) values (0, %s)
                """ % selection_id
                self._db.dbExecute(query)
        
        return


    @cherrypy.expose
    def deleteselectie(self, selection_id):
        """Button selectie verwijderen afhandelen
        """
        
        # ontvangen wordt bijvoorbeeld: btnFil353, 3 is conditie, 53 is selectie
        condition = selection_id[6:7]
        selection = selection_id[7:]
        query = """
            delete   from swc
            where    condition = %s
               and   selection_id = %s
        """ % (condition, selection)
        self._db.dbExecute(query)

        return


    @cherrypy.expose
    def deleteall(self, id):
        """Button alle selecties verwijderen afhandelen
        """

        query = """
            delete from swc
        """
        self._db.dbExecute(query)

        return


    @cherrypy.expose
    def savecondition(self, condition):
        """Button conditie afhandelen, selecties aan conditie toevoegen
        """

        # button bepalen, aangeleverd: btnCondx, btnCond verwijderen
        condition = condition[7:]

        # condition 0 samen voegen met gekozen condition         
        query = """
            insert  into swc (condition, selection_id)
            select  %s, selection_id
            from    swc
            where   condition = 0
            except
            select  %s, selection_id
            from    swc
            where   condition = %s
        """ % (condition, condition, condition)
        print 'query: ', query
        self._db.dbExecute(query)

        # condition 0 nu verwijderen
        query = """
            delete from swc
            where condition = 0
        """
        self._db.dbExecute(query)

        return


    @cherrypy.expose
    def runselection(self):
        """Button toepassen afhandelen
        """
        
        # haal alle gebruikte condities op
        query = """
            select   distinct condition
            from     swc
            where    condition > 0
            order by 1
        """
        records1 = self._db.dbGetData(query)
        
        where = ""
        # doorloop alle condities, er zijn max 4 aanwezig
        for record1 in records1:
            if len(where) > 0:
                where = where + " or "
            where = where + " ("
            
            # haal alle selections van de conditie op
            query = """
                select   swc.condition, sel.selection, sel.condition
                from     swc
                join     selections as sel
                on       swc.selection_id = sel.selection_id
                where    swc.condition = %s
                order by 1
            """ % record1['condition']
            records2 = self._db.dbGetData(query)
            tel = 0
            for record2 in records2:
                tel = tel + 1
                if tel > 1:
                    where = where + " and "
                where = where + " %s " % record2['condition']
            # sluit conditie af
            where = where + " )"

        if len(where) > 0:
            where = " where " + where

        # haal records op
        query = """
            select * from v_songs
        """ + where + " limit 100 "
        print "query: ", query
        records = self._db.dbGetData(query)
        # print "record: ", records[0]

        # stel de pagina samen
        h = searchwithselections_temp.pageRunselection(records)

        return h
