-- view voor gegevensweergave voor zoeken met selections
create or replace view v_songs
as
select 	songs.song_id
, 	max(songs.title) 	as title
, 	max(songs.artist) 	as artist
, 	max(songs.year) 	as year
, 	max(songs.tracknumber) as tracknumber
, 	max(songs.album) 	as album
, 	max(songs.albumartist) as albumartist
--      rating levert altijd een waarde op
, 	case when max(songsinfo.rating) is null then 0 else max(songsinfo.rating) end as rating
--	laatste keer gespeeld, format: yyyymmdd
,       max(to_char(played.playdate, 'yyyymmdd')) as lastplayed
--	laatste keer afgespeeld in dagen geleden
,       extract(day from now() - max(played.playdate)) as daysago
,	count(played.playdate) as played
from 	songs
left join songsinfo
on 	songs.song_id = songsinfo.song_id
left join played
on 	songs.song_id = played.song_id
group by songs.song_id ;
