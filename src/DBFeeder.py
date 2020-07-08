import pymysql
import csv
import os
import time


class DBFeeder:
    """
    connect to MySQL database
    """
    @staticmethod
    def __db_connect(host, port, user, password, database, charset):
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset=charset)
        return conn

    """
    store important list to .txt files
    """
    @staticmethod
    def __store_file(file_name, directory, content):
        file_path = os.path.join(directory, file_name)
        file = open(file_path, "w", encoding="utf-8", newline=None)
        try:
            for items in content:
                if not isinstance(items, str):
                    file.writelines(str(items) + "\n")
                else:
                    file.writelines(items + "\n")
            print("file " + file_name + " writing finished...")
        except Exception as e:
            print(e)
            file.close()
        finally:
            file.close()

    @classmethod
    def data_feeder(cls, conn, directory):
        csv_file = open(directory)
        csv_reader = csv.reader(csv_file)
        cursor = conn.cursor()
        key = 1
        new_line = []
        try:
            # delete existing table
            drop_table = "DROP TABLE IF EXISTS order_data"
            cursor.execute(drop_table)
            # create new table
            create_table = "CREATE TABLE IF NOT EXISTS order_data(" \
                           "pri_key INT AUTO_INCREMENT NOT NULL," \
                           "dates VARCHAR(45) NOT NULL," \
                           "clients VARCHAR(45) NOT NULL," \
                           "orders INT NOT NULL," \
                           "materials INT NOT NULL," \
                           "PRIMARY KEY(pri_key));"
            cursor.execute(create_table)
            # put existing data into new table
            insert_sql = "INSERT INTO aps1017.order_data VALUES(%s,%s,%s,%s,%s);"
            # date | client | order quantity | material
            for line in csv_reader:
                new_line.append(str(key))
                time_struct = time.strptime(line[0], "%m/%d/%Y")
                line[0] = time.strftime("%Y/%m/%d", time_struct)
                for items in line:
                    new_line.append(items)
                cursor.execute(insert_sql, new_line)
                conn.commit()
                print("insert line " + str(key) + "...")
                # set for next iteration
                key = key + 1
                new_line = []
            print("insertion done...")
        except Exception as e:
            print(e)
            conn.rollback()
        cursor.close()
        conn.close()

    @classmethod
    def data_washer(cls, conn):
        cursor = conn.cursor()
        find_repeat = "drop table if exists aps1017.alter_repeat, aps1017.repeat_pri_key;" \
                      "create table aps1017.alter_repeat as" \
                      "select t1.pri_key, t1.dates, t1.clients, floor(sum(t1.orders)/2) as orders, t1.materials" \
                      "from aps1017.order_data as t1 join aps1017.order_data as t2 " \
                      "where t1.pri_key != t2.pri_key and" \
                      "t1.dates = t2.dates and" \
                      "t1.clients = t2.clients and " \
                      "t1.materials = t2.materials" \
                      "group by t1.dates, t1.clients, t1.materials" \
                      "order by t1.pri_key;"
        cursor.execute(find_repeat)
        cal_sum = "create table aps1017.repeat_pri_key as" \
                  "select t1.*, 'true' as repeated " \
                  "from aps1017.order_data as t1 join aps1017.order_data as t2 " \
                  "where t1.pri_key != t2.pri_key and" \
                  "t1.dates = t2.dates and" \
                  "t1.clients = t2.clients and " \
                  "t1.materials = t2.materials" \
                  "order by t1.pri_key;"
        cursor.execute(cal_sum)
        wash_up = "delete aps1017.order_data " \
                  "from aps1017.order_data inner join aps1017.repeat_pri_key " \
                  "on aps1017.order_data.pri_key = aps1017.repeat_pri_key.pri_key" \
                  "where aps1017.order_data.pri_key = aps1017.repeat_pri_key.pri_key;"
        cursor.execute(wash_up)
        resort_down = "insert into aps1017.order_data select *from aps1017.alter_repeat;"
        cursor.execute(resort_down)
        print("repeated records deleted...")

    @classmethod
    def data_backup(cls, conn):
        cursor = conn.cursor()
        back_up = "create table if not exists aps1017.order_data_backup like aps1017.order_data;" \
                  "insert into aps1017.order_data_backup select * from aps1017.order_data;"
        print("backup done.")

    @classmethod
    def data_dispatcher(cls, conn):
        cursor = conn.cursor()
        # store materials' name
        materials_name = []
        # store clients' name
        clients_name = []
        # assign the directory of files being stored
        dir_dispatcher = os.path.dirname(os.getcwd())
        dat_base = os.path.join(dir_dispatcher, "dat")

        try:
            # find all materials name and stores them in one list
            find_materials_name = "SELECT distinct materials from aps1017.order_data order by materials;"
            cursor.execute(find_materials_name)
            m_result = cursor.fetchall()
            for items in m_result:
                materials_name.append(items[0])
            # find all clients name and stores them in one list
            find_clients_name = "SELECT distinct clients from aps1017.order_data order by clients;"
            cursor.execute(find_clients_name)
            c_result = cursor.fetchall()
            for items in c_result:
                clients_name.append(items[0])
            # dispatch data w.r.t clients' name and materials' name
            for c_index, clients in enumerate(clients_name):
                for m_index, materials in enumerate(materials_name):
                    date_dispatch = "SELECT * from aps1017.order_data where clients = '%s' and materials= " \
                                    "'%s' order by dates;" % (clients, materials)
                    cursor.execute(date_dispatch)
                    result = cursor.fetchall()
                    # create file
                    file_name = "client-" + clients + "-material-" + str(materials) + ".csv"
                    file_path = os.path.join(dat_base, file_name)
                    file = open(file_path, 'w', encoding="utf-8", newline="")
                    writer = csv.writer(file, dialect='excel')
                    title = ['pri_key', 'dates', 'clients', 'orders', 'materials']
                    writer.writerow(title)
                    for lines in result:
                        # insert info into files
                        writer.writerow(lines)
                    file.close()
            # if the only input is client
            for clients in clients_name:
                find_all_client = "SELECT pri_key,dates,clients,sum(orders) as c_orders FROM aps1017.order_data " \
                                  "where clients = '%s' group by dates order by dates; " % (clients)
                cursor.execute(find_all_client)
                result = cursor.fetchall()
                file_name = "client-" + clients + "-material-all.csv"
                file_path = os.path.join(dat_base, file_name)
                file = open(file_path, "w", encoding="utf-8", newline="")
                writer = csv.writer(file, dialect="excel")
                title = ['pri_key', 'dates', 'clients', 'orders']
                writer.writerow(title)
                for lines in result:
                    writer.writerow(lines)
                file.close()
            # if the only input is material
            for materials in materials_name:
                find_all_client = "SELECT pri_key,dates,materials,sum(orders) as m_orders FROM aps1017.order_data " \
                                  "where materials = '%s' group by dates order by dates; " % (materials)
                cursor.execute(find_all_client)
                result = cursor.fetchall()
                file_name = "client-all-" + "-material-" + str(materials) + ".csv"
                file_path = os.path.join(dat_base, file_name)
                file = open(file_path, "w", encoding="utf-8", newline="")
                writer = csv.writer(file, dialect="excel")
                title = ['pri_key', 'dates', 'materials', 'orders']
                writer.writerow(title)
                for lines in result:
                    writer.writerow(lines)
                file.close()
        except Exception as e:
            print(e)
            conn.rollback()
        cursor.close()
        conn.close()
        # store materials_name and clients_name into txt files
        file_name = "clients_name.txt"
        cls().__store_file(file_name, dat_base, clients_name)
        file_name = "materials_name.txt"
        cls().__store_file(file_name, dat_base, materials_name)
