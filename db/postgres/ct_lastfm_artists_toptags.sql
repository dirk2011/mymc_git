
-- table voor top tags, gedownload van lastfm
-- september 2014

create table lastfm_artists_toptags
(
        artist_id       serial                 primary key
,       name            character varying(200) not null
,       mbid            character varying(40)  
,       toptag1         character varying(40)
,       toptag2         character varying(40)
,       toptag3         character varying(40)
,       toptag4         character varying(40)
,       toptag5         character varying(40)
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
) ;


-- initieel vullen met records
insert into lastfm_artists_toptags 
  (name)
select distinct artist from songs ;
