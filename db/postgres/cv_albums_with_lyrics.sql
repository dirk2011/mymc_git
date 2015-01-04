-- view gemaakt jan. 2015, script is al ouder
-- toon albums welke lyrics hebben, per album aantal lyrics, en aantal songs

create view v_albums_with_lyrics
as
-- lyric info per album
select    t2.albumartist
,         t2.album
,         t2.album_id
,         t2.lyric_added
,         t2.lyrics
,         t1.songs
,         t1.lastplayed
from 
(
          -- info afgepseeld per album niveau
          select    s.album_id
          ,         count(distinct s.song_id) as songs
          ,         to_char(max(p.playdate), 'yyyy-mm-dd') lastplayed
          from      songs s  -- aantal songs van album
          left join played p -- laatste afspeeldatum
          on        s.song_id = p.song_id
          group by  s.album_id
) as t1
join
(
          -- lyric info per album
          select    s.albumartist
          ,         s.album
          ,         s.album_id
          ,         count(*) as lyrics
          ,         to_char(max(l.adddate), 'yyyy-mm-dd') lyric_added
          from      songslyrics l  -- aantal songteksten
          join      songs s        -- haal album info op, join met album
             on     l.song_id = s.song_id
          where     length(lyric) > 2
          group by  albumartist, album, album_id 
) as t2
   on     t1.album_id = t2.album_id
order by  1, 2
;
