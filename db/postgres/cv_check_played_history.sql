-- 	view om table played_history te controleren

drop view v_check_played_history ;

create or replace view v_check_played_history
as
select  1 volgnr
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99')) telling
,      'dagen' soort
,       sum(played) aantal
from 	played_history
where   month <> 0
  and	day <> 0 
union 
select  2
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99'))
,      'maanden'
,       sum(played)
from 	played_history
where   month <> 0
  and	day = 0 
union 
select  3
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99'))
,      'jaren'
,       sum(played)
from 	played_history
where   month = 0
  and	day = 0 
union
select  4
,	count(*)
,      'records'
,       0
from	played_history
union 
--	controleer met details
select  5
,	0
,      'controle'
,       count(*)
from 	played 
order by 1 ;

--      controle
select  *
from    v_check_played_history ;
