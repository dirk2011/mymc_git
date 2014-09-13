-- table artists
-- 2014-09-13
-- doel van de table, vastleggen artist_id in songs, zodat
--                    html pagina's gemakkelijk met elkaar kunnen communiceren

drop table artists ;

create table artists
(
        artist_id       serial                 primary key
,       artist          character varying(200) not null unique
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
) ;

drop table albumartists ;

create table albumartists
(
        albumartist_id  serial                 primary key
,       albumartist     character varying(200) not null unique
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
) ;

drop table albums ;

create table albums
(
        album_id        serial                 primary key
,       albumartist     character varying(200) not null
,       album           character varying(200) not null
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
,	unique (albumartist, album)
) ;

alter table songs add 	artist_id	integer ;
alter table songs add 	albumartist_id	integer ;
alter table songs add 	album_id	integer ;


--# voorbeeld voor een id veld:
--# song_id         integer        primary  key autoincrement
--# voorbeeld voor een unique veld:
--# mc_id           integer        unique 

-- test
-- insert into songs (title, album, artist, albumartist, track, length, size) 
-- values ('Dancing Queen', 'Arrival', 'Abba', 'Abba', 1, 241, 5) ;

