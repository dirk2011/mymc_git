-- parameter tabel


drop table parameters ;

create table parameters
(
        id              serial                 primary key
,       parameter       character varying(100) not null           -- parameter
,       parameter_desc  character varying(100) not null           -- parameter description
,       number_value    integer                                   -- number value
,       string_value    character varying(100)
,       date_value      timestamp without time zone
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
,       unique(parameter)
) ;


insert into parameters (parameter, parameter_desc, number_value)
    values ('played_period_albumsartists', 'laatst verwerkte played_id', 0) ;
update parameters set number_value = 0 where parameter = 'played_period_albumsartists' ;

select parameter, number_value
from parameters
where parameter = 'played_period_albumsartists' ;


insert into parameters (parameter, parameter_desc, number_value)
    values ('played_period_albums', 'laatst verwerkte played_id', 0) ;
update parameters set number_value = 0 where parameter = 'played_period_albums' ;

select parameter, number_value
from parameters
where parameter = 'played_period_albums' ;


