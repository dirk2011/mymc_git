# postgresql database export teruglezen

psql -d dbmc -h bmc -p 5432 -U pi -f dbmc-restore.dump
