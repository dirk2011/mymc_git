# -*- coding: utf-8 -*-

"""Module selections.

Bevat class SearchWithSelections, 
zoeken met selecties.

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


class searchWithSelections(object):
    """Zoeken met selections
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
        """Index pagina, toon inhoud swc table (search with selections).
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
        """Button selectie afhandelen, er is een nieuwe selectie gekozen.
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
        """Button selectie verwijderen afhandelen.
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
        """Button alle selecties verwijderen afhandelen.
        """

        query = """
            delete from swc
        """
        self._db.dbExecute(query)

        return


    @cherrypy.expose
    def savecondition(self, condition):
        """Button conditie afhandelen, selecties aan conditie toevoegen.
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
    def saveSuperSelection(self, txtId=0, txtCode="#", txtDescr="#"):
        """Button saveSuperSelection afhandelen
        Nieuwe superselectie opslaan.
        """
        
        print "saveSuperSelection txtId", txtId, "txtCode", txtCode, "txtDesc", txtDescr
        
        # hoofdrecord
        if len(txtId) == 0:
            # nieuw !
            query = """
                insert into superselections (ss_code, ss_descr)
                values ('%s', '%s')
                """ % (q(txtCode), q(txtDescr))
            self._db.dbExecute(query)
            
            # zoek Id op van zojuist opgeslagen record
            query = """
                select ss_id from superselections
                where ss_code = '%s'
            """ % q(txtCode)
            records = self._db.dbGetData(query)
            
            if len(records) == 1:
                txtId = records[0]['ss_id']
                print "nieuwe txtId: ", txtId
            
        else:
            # wijziging
            query = """
                update superselections set ss_code = '%s', ss_descr = '%s'
                where ss_id = %s
            """ % (q(txtCode), q(txtDescr), txtId)
        self._db.dbExecute(query)

        ## details opslaan
        # oude verwijderen
        query = """
            delete from superselections_details
            where ss_id = %s
        """ % txtId
        self._db.dbExecute(query)
        # nieuwe opslaan
        query = """
            insert into superselections_details (ss_id, condition, selection_id)
            select %s, condition, selection_id
            from    swc
            where   condition > 0
        """ % txtId
        self._db.dbExecute(query)        


    @cherrypy.expose
    def deleteSuperSelection(self, txtId=0):
        """Button deleteSuperSelection afhandelen.
        SuperSelectie verwijderen.
        """
        
        print "deleteSuperSelection txtId", txtId

        if len(txtId) != 0:
            query = """
                delete from superselections
                where ss_id = %s 
            """ % txtId
            self._db.dbExecute(query)
            query = """
                delete from superselections_details
                where ss_id = %s
            """ % txtId
            self._db.dbExecute(query)


    @cherrypy.expose
    def loadSuperSelection(self, txtId=0):
        """Button Laden SuperSelection afhandelen.
        """

        print "loadSuperSelection txtId", txtId

        # swc eerst leegmaken
        query = """
            delete from swc 
        """
        self._db.dbExecute(query)

        # swc vullen vanuit superselections_details
        query = """
            insert into swc (condition, selection_id)
            select condition, selection_id
            from superselections_details
            where ss_id = %s
            """ % txtId
        self._db.dbExecute(query)        


    @cherrypy.expose
    def manageSuperSelections(self):
        """Beheer super selections pagina.
        """
        
        # haal conditions op
        query = """
            select   *
            from     superselections
            order by ss_code
        """
        records = self._db.dbGetData(query)
        
        h = searchwithselections_temp.pageManageSuperSelections(records)
        
        return h


    @cherrypy.expose
    def runselection(self):
        """Button toepassen afhandelen, zoek songs via de selecties.
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
