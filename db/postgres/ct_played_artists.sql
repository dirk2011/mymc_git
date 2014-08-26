
-- 
-- table voor history per tijdvak, artiest, album, songs
-- 

drop table played_artist ;

create table played_artists
(
        history_id	serial         		primary key
        -- period = day, week, month, quarter, half year, year, all
,       period		character varying(20) 	not null
	-- aat = album, artist, title
,	aat		character varying(20)	not null
,       artist		character varying(200)	not null
,	album		character varying(200)
,	title		character varying(200)
	-- played = aantal
,       played		integer        		not null
,       adddate		timestamp 		without time zone NOT NULL DEFAULT now()
) ;


create unique index played_artists_i1 on played_artists (period, aat, artist, album, title) ;


