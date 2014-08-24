
-- 
-- table voor history per tijdvak
-- 

drop table played_history ;

create table played_history
(
        history_id      serial         primary key
,       year            integer        not null
,       month           integer        not null
,       day             integer        not null
,       played          integer        not null
,       adddate         timestamp 	without time zone NOT NULL DEFAULT now()
) ;


create unique index played_history_i1 on played_history (year, month, day) ;


-- test data

insert into played_history (year, month, day, played) values (2014, 8, 16, 25);
insert into played_history (year, month, day, played) values (2014, 8, 17, 21);
insert into played_history (year, month, day, played) values (2014, 8, 18, 32);

insert into played_history (year, month, day, played) values (2014, 8, 0, 91);

insert into played_history (year, month, day, played) values (2014, 0, 0, 91);

select * from played_history ;

