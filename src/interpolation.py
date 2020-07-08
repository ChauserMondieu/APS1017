import pymysql
import os
import time
import csv


DAY_TIME = 24*60*60


def db_connect(host, port, user, password, database, charset):
    return pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)


def data_interpolation(conn, dat_dir, alg_dat_dir):
    """
    step1: define max time and min time in sec
    step2: input data and tags
    """
    cursor = conn.cursor()
    # list for tages
    clients_name = []
    materials_name = []
    # list for algorithm data: dates, orders
    dates = []
    dates_series = []
    orders = []

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

    # input clients and materials name
    clients_file_name = "clients_name.txt"
    tag_input(clients_file_name, dat_dir, clients_name)
    materials_file_name = "materials_name.txt"
    tag_input(materials_file_name, dat_dir, materials_name)

    # choose designated files
    file_name = "client-c1-material-12404641.csv"
    # get dates info
    data_input(file_name, dat_dir, dates, 1)
    for index, items in enumerate(dates):
        dates[index] = timestamp_transfer(items)
        dates_series.append((dates[index]-min_time)/DAY_TIME)
    print(dates_series)
    # get orders info
    data_input(file_name, dat_dir, orders, 3)



# def interpolation(dates, orders):



def timestamp_transfer(ori_time):
    # dates format: YYYY/mm/dd
    return time.mktime(time.strptime(ori_time, "%Y/%m/%d"))


def tag_input(file_name, dir, structure):
    """
    :param file_name: name of input file
    :param dir: name of data directory
    :param structure: name of list that data are to stored
    :return: None
    """
    file_path = os.path.join(dir, file_name)
    file = open(file_path, "r", encoding="utf-8")
    for lines in file:
        structure.append(lines)
    file.close()


def data_input(file_name, dir, structure, pos):
    """
    :param file_name: name of input file
    :param dir: name of data directory
    :param structure: name of list that data are to stored
    :param pos: 0-pri_key; 1-dates; 2-clients; 3-orders; 4-materials
    :return: None
    """
    file_path = os.path.join(dir, file_name)
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for lines in reader:
            structure.append(lines[pos])


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