-- view voor gegevensweergave voor zoeken met selections

-- 13 okt 2014, firstplayed, lq, lw, lm, toegevoegd
-- 15 okt 2014, length toegevoegd
-- 11 nov 2014, songslyrics toegevoegd

drop view v_songs ;

create view v_songs
as
select 	songs.song_id
,       max(songs.title) 	as title
,       max(songs.artist) 	as artist
,       max(songs.artist_id)   as artist_id
,       max(songs.year) 	as year
,       max(songs.tracknumber) as tracknumber
,       max(songs.album) 	as album
,       max(songs.album_id)    as album_id
,       max(songs.albumartist) as albumartist
,       max(songs.albumartist_id) as albumartist_id
--      rating levert altijd een waarde op
,       case when max(songsinfo.rating) is null then 0 else max(songsinfo.rating) end as rating
--	eerste keer afgespeeld
,       to_char(min(played.playdate), 'dd-mm-yyyy') as firstplayed
--      laatste keer gespeeld, format: yyyymmdd
,       to_char(max(played.playdate), 'dd-mm-yyyy') as lastplayed
--      laatste keer afgespeeld in dagen geleden, is 999 als nog nooit
,	case when extract(day from now() - max(played.playdate)) is null then 999
             else extract(day from now() - max(played.playdate)) end as daysago
,       count(played.playdate) as played
,       sum(case when extract(day from now() - played.playdate) <= 7 then 1
                 else 0 end) as lw	-- last week
,       sum(case when extract(day from now() - played.playdate) <= 30 then 1
                 else 0 end) as lm	-- last month
,       sum(case when extract(day from now() - played.playdate) <= 90 then 1
                 else 0 end) as lq	-- last quarter
,       max(songs.length) as length
        -- 11 nov 2014, no/yes for lyrics
,	case when max(songslyrics.song_id) is null then 'No' else 'Yes' end as lyric
from 	songs
left join songsinfo
on 	songs.song_id = songsinfo.song_id
left join played
on 	songs.song_id = played.song_id
left join songslyrics	-- bevat maar 1 record per song
on      songs.song_id = songslyrics.song_id
group by songs.song_id ;



,       max(to_char(songs.length / 60, '99') || ':' || trim(to_char(length - (length / 60) * 60, '00')))
                 as length
