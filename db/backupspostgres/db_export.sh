#!/bin/bash 
# export maken van postgresql database

cd '/media/rasp163-v/mymc/db/backupspostgres'

BACKUPDATE=`date +%Y%m%d-%H%M`

pg_dump -h mc -p 5432 -U pi dbmc > ./exports/${BACKUPDATE}-dbmc.dump
