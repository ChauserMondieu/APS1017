drop table aps1017.order_data;
create table aps1017.order_data like aps1017.order_data_backup;
insert into aps1017.order_data select * from aps1017.order_data_backup;

# select * from aps1017.order_data into outfile "dir";
# create table aps1017.order_data_b like aps1017.order_data;
# load data infile "dir" into table aps1017.order_data_b;
# this method is much faster than insert into