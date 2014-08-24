-- postgres, create statement voor table songs
-- 2014-08-24

drop table songs ;

create table songs
(
        song_id         serial                 primary key
,       title           character varying(200) not null
,       album           character varying(200) not null
,       artist          character varying(200) not null
,       albumartist     character varying(200) not null
,       tracknumber     integer                not null
,       year            integer        
,       genre           character varying(200)
,       length          integer                not null
,       bitrate         integer                not null
,       size            integer                not null
,       location        character varying(255) not null
,       filename        character varying(255) not null
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
) ;



--# voorbeeld voor een id veld:
--# song_id         integer        primary  key autoincrement
--# voorbeeld voor een unique veld:
--# mc_id           integer        unique 

-- test
-- insert into songs (title, album, artist, albumartist, track, length, size) 
-- values ('Dancing Queen', 'Arrival', 'Abba', 'Abba', 1, 241, 5) ;

