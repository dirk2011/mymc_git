#!/bin/bash 
# export maken van postgresql database

BACKUPDATE=`date +%Y%m%d`

pg_dump -h mc -p 5432 -U pi dbmc > ./exports/${BACKUPDATE}-dbmc.dump
