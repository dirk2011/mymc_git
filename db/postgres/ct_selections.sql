-- table for storage selections

drop table selections ;

create table selections
(
         selection_id    serial                 primary key
,       selection       character varying(30)  not null
,       description     character varying(50)  not null
,       condition       character varying(100) not null
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
, unique(selection)
, check(length(trim(selection)) > 0)
, check(length(trim(condition)) > 0)
) ;

