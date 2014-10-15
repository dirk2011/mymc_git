# sqlist create

drop table played ;

create table played
(
        played_id       serial         primary key
,       song_id         integer        not null
,       playdate        timestamp 	without time zone NOT NULL DEFAULT now()

) ;

create index played_song_id on played(song_id) ;


-- test
insert into played (song_id) values (1001) ;
insert into played (song_id) values (151) ;

select * from played ;

delete from played ;

-- eof
