-- 	view om table played_history te controleren

create or replace view v_check_played_history
as
select  1 volgnr, 'dagen' soort, sum(played) aantal
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99')) telling
from 	played_history
where   month <> 0
  and	day <> 0 
union 
select  2, 'maanden', sum(played)
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99'))
from 	played_history
where   month <> 0
  and	day = 0 
union 
select  3, 'jaren', sum(played)
,	count(distinct to_char(year, '9999') || to_char(month, '99') || to_char(day, '99'))
from 	played_history
where   month = 0
  and	day = 0 
union
select  4, 'records', 0
,	count(*)
from	played_history
union 
--	controleer met details
select 	5, 'controle', count(*)
,	0
from 	played 
order by 1 ;