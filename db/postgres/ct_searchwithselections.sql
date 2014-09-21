-- search with conditions (swc), zoeken met selecties
-- 2014-09-21

drop table swc ;

create table swc
-- sws: seearch with conditions/selections
(
        sws_id          serial                 primary key
,       condition       integer                not null
,       selection_id    integer                not null
,       adddate         timestamp without time zone NOT NULL DEFAULT now()
,	check (condition between 0 and 4)
,	unique (condition, selection_id)
) ;


-- test data
insert into swc (condition, selection_id) values (1, 10) ;
insert into swc (condition, selection_id) values (1, 57) ;

insert into swc (condition, selection_id) values (2, 10) ;
insert into swc (condition, selection_id) values (2, 57) ;

insert into swc (condition, selection_id) values (3, 10) ;
insert into swc (condition, selection_id) values (3, 57) ;

insert into swc (condition, selection_id) values (4, 10) ;
insert into swc (condition, selection_id) values (4, 57) ;

-- test opvraging
select    swc.condition, swc.selection_id, s.selection
from      swc    -- selection with conditions
join	  selections as s
on 	  swc.selection_id = s.selection_id
where     swc.condition != 0
order by  swc.condition, swc.selection_id ;
