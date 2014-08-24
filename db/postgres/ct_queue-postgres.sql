-- queue table

-- vullen als queue gevuld wordt, en legen als queue geleegd wordt
-- doel: song_id als info, bij raadplegen queue kunnen tonen

drop table queue ;

create table queue
(
        queue_id        serial		primary key
,       song_id         integer        not null check (song_id > 0)
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
) ;

