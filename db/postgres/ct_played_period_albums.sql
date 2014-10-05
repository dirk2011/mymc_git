
-- postgres, played albums per month
-- 2014-10


drop table played_period_albums ;

create table played_period_albums
(
        id                serial                   primary key
,       adddate           timestamp without time zone NOT NULL DEFAULT now()
,       yr                integer                  not null
,       month             integer                  not null
,       album_id          integer                  not null
,       album             character varying(200)   not null
,       albumartist_id    integer                  not null
,       albumartist       character varying(200)   not null
,       album_songs       integer                  not null   -- aantal songs dat een album heeft
,       album_folder_jpg  character varying(300)   not null   -- folder.jpg locatie
,       played_first     date                      not null
,       played_last      date                      not null
,       played_songs      integer                  not null   -- aantal gespeeld
,       unique (yr, month, album_id)
) ;

Controleer of tabel goed gevuld is, controleer aantal played_songs
select 'played_period_albums', sum(played_songs) from played_period_albums
union
select 'played', count(*) from played ;


Controle of tabel goed gevuld is, controleer aantal album in één maand.

select s.album_id, count(*)
from played as p
join songs as s
on p.song_id = s.song_id
where to_char(p.playdate, 'yyyymm') = '201409'
group by s.album_id ;


Controleer aantal unieke, albumartists

select s.albumartist_id, count(*)
from played as p
join songs as s
on p.song_id = s.song_id
where to_char(p.playdate, 'yyyymm') = '201409'
group by s.albumartist_id 
order by 2 desc ;





STAPPEN om tabel te vullen:
bepaal max(played_id) van played_albums
  als niet gevonden, dan stel op 0
doorloop played_songs vanaf played_id, werk deze tabel bij
     bepaal: jaar, maand, zoek op: album_id
     zoek jaar, maand, album_id op in tabel
     indien bestaat lees played_albums record
     als niet bestaat:
	zoek op album
	zoek op albumartist_id
	zoek op albumartist_name
	zoek op aantal album_songs
	zoek op album_folder_jpg
	zet played_songs := 0
     als songs_played.date < played_first, played_first := songs_played.date
     als songs_played.date > played_last,  played_last  := songs_played.date
     vul played_id met played.played_id
     verhoog played_songs met 1
 
 
 
 select case when max(played_id) is null then 0 else max(played_id) end from played_albums ;

 
drop function testje() ;

create or replace function testje() RETURNS integer as 
 $$
 declare
    rec  record ;
    teller integer ;
 begin
    select case when max(played_id) is null then 0 else max(played_id) end from played_albums ;
    teller := 0 ;
    for rec in select * from queue loop
      teller := teller + 1 ;
    end loop ;
    raise notice 'Return value is: %', teller;
    return teller ;
 end ;
 $$ 
 LANGUAGE plpgsql;
 