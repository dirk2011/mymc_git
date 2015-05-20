# -*- coding: utf-8 -*-

"""Module tags

Bevat class om tags te muteren

"""


__author__  = 'dp'
__date__    = '2015-04'


# pylint: disable=C0103, C0301, R0201
# C0103 - naming convention
# C0301 - lengte van de regels
# R0201 - method could be a function


import cherrypy             # cherrypy de webinterface
import mymc_html            # web pagina's
reload(mymc_html)
import tagsbeheer_temp
reload(tagsbeheer_temp)
from dbfunc import MyDB
from dbfunc import q


class tagsbeheer(object):
    """Muteren van tags
        @since: 2015-04
        @version: 1
    """

    def __init__(self):
        """Database verbinding maken.
        @ivar _db: database  
        """
        self._db = MyDB() 


    @cherrypy.expose
    def index(self):
        """Hoofd ingang muteren tags
        Pagina geeft een lijst van bestaande tags
        """

        query = """
            select      tag_id
            ,           tag
            ,           description
            ,           to_char(adddate, 'yyyy-mm-dd') as adddate
            from        tagslov
            order by    tag
        """
        records = self._db.dbGetData(query)
        print "tagslov records: ", records

        h = tagsbeheer_temp.pageTagsList(records)

        return h


    @cherrypy.expose
    def new(self):
        """Buttton new afhandelen, om nieuwe tags toe te voegen
        """
        
        # leeg record aanmaken
        record = {'tag': "", 'description': "",  'tag_id': ""}
        records = [record]
        
        h = tagsbeheer_temp.pageTag(records)
        
        return h


    @cherrypy.expose
    def pageTag(self, id):
        """Pagina voor het muteren van één tag.
        """

        query = """
            select      tag_id
            ,           tag
            ,           description
            ,           to_char(adddate, 'yyyy-mm-dd') as adddate
            from        tagslov
            where       tag_id = %s
            order by    tag
        """ % id
        records = self._db.dbGetData(query)
        print "pageTag, records: ", records

        h = tagsbeheer_temp.pageTag(records)
        
        return h


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save(self, txtCode="#", txtDescr="#", txtId="#"):
        """Button saven afhandelen, een tag opslaan.
        """

        # probeer een update, deze lukt indien conditie al bestaat
        if len(txtId) > 0:
            query = """
                update  tagslov set tag = '%s'
                ,       description = '%s'
                where   tag_id = '%s'
            """ % (q(txtCode), q(txtDescr), txtId)
            # print "\nupdate query: ", query, '\n'
            self._db.dbExecute(query)
        
        # probeer een insert, deze lukt indien conditie nog niet bestaat
        query = """
            insert into tagslov (tag, description) 
            select '%s', '%s'
            where not exists (select 1 from tagslov where tag = '%s') 
        """ % (q(txtCode), q(txtDescr), q(txtCode))
        self._db.dbExecute(query)

        return 

################################################################################

    @cherrypy.expose
    def delete(self, txtCode="#"):
        """Button delete afhandelen, een tag verwijderen. 
        """

        query = "delete from tagslov where tag = '%s'" % txtCode
        self._db.dbExecute(query)

        return

