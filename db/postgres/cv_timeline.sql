--------------------------------------------------------------------------------
-- view voor afgespeelde 1000-tallen
-- 2014-10-19
--------------------------------------------------------------------------------


-- view berekent en toont op welke datum 1000-tallen waren afgespeeld
create view v_timeline 
as
select     t1.sort
,          to_char(t1.playdate, 'yyyy-mm-dd') as playdate
,          t1.played as played
,          extract(day from t1.playdate - t2.playdate) as days
from       v_timeline_01 as t1
left join  v_timeline_01 as t2
   on      t1.sort = t2.sort + 1 
order by   1 desc;


-- # 2e view is nodig voor de 1e 
create view v_timeline_01 as
-- 1e
select *
from  (
       select playdate
       ,      1 as played
       ,      0 as sort
       from   played
       order by playdate
       limit 1 ) b
union all
-- 1000-tallen
select playdate
,      i
,      i2
from  (
       select *
       , row_number() over (order by playdate) as i
       , row_number() over (order by playdate) / 1000 as i2
       from played
       order by playdate
      ) as a
where (i / 1000) * 1000 = i 
union all
-- laatste
select *
from  (
       select playdate
       ,      row_number() over (order by playdate) as i
       , (row_number() over (order by playdate) / 1000) + 1 as i2
       from   played
       order by playdate desc
       limit 1 
      ) c ;

-- eof
