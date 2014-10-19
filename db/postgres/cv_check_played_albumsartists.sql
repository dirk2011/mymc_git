
-- aantal afgespeeld
select  sum(played_songs)
from played_period_albumsartists ;

-- eerste dag
select yr, month, played_first
from played_period_albumsartists 
order by 1, 2, 3
limit 1 ;

-- laatste dag
select yr, month, played_last
from played_period_albumsartists 
order by 3 desc
limit 1 ;

-- distinct played_first
select   count(*)
from    (
         select   distinct played_first
         from     played_period_albumsartists 
        ) as a
;

-- distinct albumartist
select   count(*)
from    (
         select   distinct albumartist
,                 albumartist_id
         from     played_period_albumsartists 
        ) as a
;

