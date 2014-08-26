""" Convert records from sqlite3 database to postgresql database
"""


import sys
import codecs               # voor utf-8 bestanden
import os
import os.path
import sys

import sqlite3              # sqlite database
import psycopg2             # postgres db
import psycopg2.extras      # dictionary cursor

# sqlite3 database
DBNAME = "/media/rasp163-v/mymc/db/music_collection.db"


class Convert():

    def __init__(self):
        self.sqlcon = None
        self.sqlcursor = None
        self.pgcon = None
        self.pgcursor = None


    def sqlOpen(self):
        """open sqlite3 database
        """

        if self.sqlcon is None:
            self.sqlcon = sqlite3.connect(DBNAME)
            self.sqlcon.row_factory = sqlite3.Row
            self.sqlcursor = self.sqlcon.cursor()
            return 1

        return 0
        

    def pgOpen(self):
        """open postgres database
        """

        if self.pgcon is None:
            ### postgresql
            try:
                self.pgcon = psycopg2.connect(database='dbmc', user='pi', host="mc", port="5432")
                ## gewone cursor
                # Mc.cursor = Mc.connection.cursor()
                ## dictionary cursor
                self.pgcursor = self.pgcon.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.pgcursor.execute('select version()')
                ver = self.pgcursor.fetchone()
                print ver
                return 1

            except psycopg2.DatabaseError, e:
                print 'Error %s' % e

        return 0


    def sqlGetData(self, query="select 'leeg' as leeg ;"):
        """ input query uitvoeren, en data terug leveren
            input: een query
            output: de data in de vorm: list, genest meerdere dictionries
        """

        # data ophalen

        # open database
        self.sqlOpen()

        # print 'query', query # zet aan voor debuggen
        self.sqlcursor.execute(query)
        recordset = self.sqlcursor.fetchall()

        hrecords = []
        tel = 0
        for record in recordset:
            hrecord = {}
            tel = tel + 1
            for sleutel in record.keys():
                hrecord[sleutel] = record[sleutel]
            hrecords.append(hrecord)
        # print hrecords # zet aan voor debuggen 

        return hrecords


    def pgStoreData(self, query, records):
        """gegevens opslaan in pg database
        """

        self.pgOpen()
        for record in records:
            print (query % record)
            self.pgcursor.execute(query % record)
            self.pgcon.commit()



a = Convert()
a.sqlOpen()
a.pgOpen()

records = a.sqlGetData("select * from played order by playdate ")

# played_id verwijderen uit dictionary
oldrecords = records
records = []
for record in oldrecords:
    del record['played_id']
    records.append(record)
print len(records)

# opslaan in pg
query = """insert into played (playdate, song_id) values (
            TO_TIMESTAMP('%(playdate)s', 'YYYY-MM-DD HH24-MI-SS'), %(song_id)s)"""
a.pgStoreData(query, records)

    
