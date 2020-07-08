drop table if exists aps1017.alter_repeat, aps1017.repeat_pri_key;

# create new table alter_repeat stroing sum of repeated records
create table aps1017.alter_repeat as
select t1.pri_key, t1.dates, t1.clients, floor(sum(t1.orders)/2) as orders, t1.materials
from aps1017.order_data as t1 join aps1017.order_data as t2 
where t1.pri_key != t2.pri_key and
t1.dates = t2.dates and
t1.clients = t2.clients and 
t1.materials = t2.materials
group by t1.dates, t1.clients, t1.materials
order by t1.pri_key;

# create table repeat_pri_key storing all repeated records
create table aps1017.repeat_pri_key as
select t1.*, "true" as repeated 
from aps1017.order_data as t1 join aps1017.order_data as t2 
where t1.dates = t2.dates and
t1.clients = t2.clients and 
t1.orders != t2.orders and
t1.materials = t2.materials
order by t1.pri_key;

# delete all repeated records in table order_data
delete aps1017.order_data 
from aps1017.order_data inner join aps1017.repeat_pri_key 
on aps1017.order_data.pri_key = aps1017.repeat_pri_key.pri_key;

# insert content of alter_repeat back into order_data
insert into aps1017.order_data select *from aps1017.alter_repeat;
