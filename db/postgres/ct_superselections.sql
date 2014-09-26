-- superselections
-- tabellen om selecties met condities in op te slaan

drop table superselections ;

create table superselections (
        ss_id           serial                 primary key
,	ss_code         character varying(30)  not null
,	ss_descr        character varying(80)  not null
,       adddate         timestamp              without time zone NOT NULL DEFAULT now()
,	unique (ss_code)
) ;



drop table superselections_details ;

create table superselections_details (
        ssd_id          serial                 primary key
,       ss_id           integer                not null
,       condition       integer                not null
,       selection_id    integer                not null
,       adddate         timestamp              without time zone NOT NULL DEFAULT now()
,	unique (ss_id, condition, selection_id)
,	check (condition between 1 and 4)
) ;

-- eof
