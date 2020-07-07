import pymysql
import csv
import os
import time

ADD_TABLE = False


def db_connect(host, port, user, password, database, charset):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset=charset)
    return conn


def data_feeder(conn, dir):
    csv_file = open(dir)
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
        insertsql = "INSERT INTO aps1017.order_data VALUES(%s,%s,%s,%s,%s);"
        # date | client | order quantity | material
        for line in csv_reader:
            new_line.append(str(key))
            time_struct = time.strptime(line[0], "%m/%d/%Y")
            line[0] = time.strftime("%Y/%m/%d", time_struct)
            for items in line:
                new_line.append(items)
            cursor.execute(insertsql, new_line)
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


def data_dispatcher(conn):
    cursor = conn.cursor()
    # store materials' name
    materials_name= []
    # store clients' name
    clients_name = []
    # assign the directory of files being stored
    dir_dispatcher = os.path.dirname(os.getcwd())
    base = os.path.join(dir_dispatcher, "dat")

    try:
        # find all materials name and stores them in one list
        find_materials_name = "SELECT distinct materials from aps1017.order_data order by materials;"
        cursor.execute(find_materials_name)
        m_result = cursor.fetchall()
        for items in m_result :
            materials_name.append(items[0])
        # find all clients name and stores them in one list
        find_clients_name = "SELECT distinct clients from aps1017.order_data order by clients;"
        cursor.execute(find_clients_name)
        c_result = cursor.fetchall()
        for items in c_result :
            clients_name.append(items[0])
        # dispatch data w.r.t clients' name and materials' name
        for c_index, clients in enumerate(clients_name):
            for m_index, materials in enumerate(materials_name):
                date_dispatch = "SELECT * from aps1017.order_data where clients = '%s' and materials= '%s' order by " \
                                "dates;" % (clients, materials)
                cursor.execute(date_dispatch)
                result = cursor.fetchall()
                # create file
                file_name = "client-" + clients + "-material-" + str(materials) + ".csv"
                file_path = os.path.join(base, file_name)
                file = open(file_path, 'w', encoding="utf-8", newline="")
                for lines in result:
                    # insert info into files
                    writer = csv.writer(file, dialect='excel')
                    writer.writerow(lines)
                file.close()
        # if the only input is client
        for clients in clients_name:
            find_all_client = "SELECT dates,clients,sum(orders) as c_orders FROM aps1017.order_data " \
                              "where clients = '%s' group by dates order by dates; " % (clients)
            cursor.execute(find_all_client)
            result = cursor.fetchall()
            file_name = "client-" + clients + "-material-all.csv"
            file_path = os.path.join(base, file_name)
            file = open(file_path, "w", encoding="utf-8", newline="")
            for lines in result:
                writer = csv.writer(file, dialect="excel")
                writer.writerow(lines)
            file.close()
        # if the only input is material
        for materials in materials_name:
            find_all_client = "SELECT dates,materials,sum(orders) as m_orders FROM aps1017.order_data " \
                              "where materials = '%s' group by dates order by dates; " % (materials)
            cursor.execute(find_all_client)
            result = cursor.fetchall()
            file_name = "client-all-" + "-material-" + str(materials) + ".csv"
            file_path = os.path.join(base, file_name)
            file = open(file_path, "w", encoding="utf-8", newline="")
            for lines in result:
                writer = csv.writer(file, dialect="excel")
                writer.writerow(lines)
            file.close()
    except Exception as e:
        print(e)
        conn.rollback()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    base = os.path.dirname(os.getcwd())
    dat_name = r"dat\APS1017 Order data for Project.csv"
    dir = os.path.join(base, dat_name)

    host = "192.168.5.12"
    port = 3306
    user = "develop"
    password = "APS1017s"
    database = "aps1017"
    charset = "utf8"
    conn = db_connect(host, port, user, password, database, charset)
    if ADD_TABLE is True:
        data_feeder(conn, dir)
    data_dispatcher(conn)
