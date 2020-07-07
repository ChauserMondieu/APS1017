import pymysql
import os
import time


def db_connect(host, port, user, password, database, charset):
    return pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)


def data_interpolation(conn, dat_dir, alg_dat_dir):
    """
    step1: define max time and min time in sec
    """
    cursor = conn.cursor()
    clients_name = []
    materials_name = []
    # fetch the max date in dates
    get_max = "select max(dates) from aps1017.order_data;"
    cursor.execute(get_max)
    result = cursor.fetchall()
    max_date = (result[0])[0]
    max_time = timestamp_transfer(max_date)
    # fetch the min date in dates
    get_min = "select min(dates) from aps1017.order_data;"
    cursor.execute(get_min)
    result = cursor.fetchall()
    min_date = (result[0])[0]
    min_time = timestamp_transfer(min_date)

    file_name = "clients_name.txt"
    tag_input(file_name, dat_dir, clients_name)


def timestamp_transfer(ori_time):
    # dates format: YYYY/mm/dd
    return time.mktime(time.strptime(ori_time, "%Y/%m/%d"))


def tag_input(file_name,dir, structure):
    file_path = os.path.join(dir,file_name)
    file = open(file_path, "r", encoding="utf-8")
    for lines in file:
        structure.append(lines)
    file.close()

if __name__ == "__main__":
    base = os.path.dirname(os.getcwd())
    dat_name = "dat"
    alg_name = "alg_dat"
    dat_dir = os.path.join(base, dat_name)
    alg_dat_dir = os.path.join(base, alg_name)

    host = "192.168.5.12"
    port = 3306
    user = "develop"
    password = "APS1017s"
    database = "aps1017"
    charset = "utf8"
    conn = db_connect(host, port, user, password, database, charset)
    data_interpolation(conn, dat_dir, alg_dat_dir)