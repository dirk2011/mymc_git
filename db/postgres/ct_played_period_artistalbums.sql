-- tabel voor afgespeelde albumartiesten per periode (jaar / maand)

drop table played_period_albumsartists ;

create table played_period_albumsartists
(
        id                serial                   primary key
,       adddate           timestamp without time zone NOT NULL DEFAULT now()
,       yr                integer                  not null
,       month             integer                  not null
,       albumartist_id    integer                  not null
,       albumartist       character varying(200)   not null
,       played_first      date                     not null
,       played_last       date                     not null
,       played_songs      integer                  not null   -- aantal gespeeld
,       unique (yr, month, albumartist_id)
) ;

