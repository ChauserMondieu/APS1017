drop table aps1017.order_data;
create table aps1017.order_data like aps1017.order_data_backup;
insert into aps1017.order_data select * from aps1017.order_data_backup;