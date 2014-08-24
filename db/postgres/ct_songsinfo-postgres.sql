# sqlist create

drop table songsinfo ;

create table songsinfo
(
        song_id         integer	primary key  check (song_id > 0)
,       rating          integer	not null check(rating between 0 and 5)
,	adddate         timestamp 	without time zone NOT NULL DEFAULT now()
) ;

delete from songsinfo ;

insert into songsinfo (song_id, rating) values (1, 5) ;

select * from songsinfo ;

-- einde
