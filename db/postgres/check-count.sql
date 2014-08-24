-- controleer aantal records in de db
select 'songs', count(*) from songs 
union all
select 'songsinfo', count(*) from songsinfo 
union all
select 'played', count(*) from played
union all
select 'played_history', count(*) from played_history 
union all
select 'queue', count(*) from queue 
order by 1 ;