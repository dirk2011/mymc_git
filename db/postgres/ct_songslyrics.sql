-- postgres, create table
-- 2014-11-09

drop table songslyrics ;

create table songslyrics
(
        song_id         integer	               primary key
,       lyric           character varying(4000)       not null
,       adddate         timestamp without time zone   NOT NULL DEFAULT now()
) ;

alter table songslyrics
    alter column lyric type character varying(8000) ;
