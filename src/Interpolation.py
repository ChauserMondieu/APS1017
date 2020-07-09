import pymysql
import os
import time
import csv
from itertools import islice


class Interpolation(object):
    __DAY_TIME = 24 * 60 * 60
    # list for algorithm data: dates, orders
    __dates = []
    __dates_series = []
    __orders = []
    # list for tages
    __clients_name = []
    __materials_name = []
    # min and max date
    __min_date = []
    __max_date = []
    __max_time = 0
    __min_time = 0

    def __init__(self):
        # list for algorithm data: dates, orders
        __dates = []
        __dates_series = []
        __orders = []
        # list for tages
        __clients_name = []
        __materials_name = []
        # min and max date
        __min_date = []
        __max_date = []
        __max_time = 0
        __min_time = 0

    @classmethod
    def get__dates(cls):
        return cls().__dates

    @classmethod
    def get__dates_series(cls):
        return cls().__dates_series

    @classmethod
    def get__orders(cls):
        return cls().__orders

    @classmethod
    def get__clients_name(cls):
        return cls().__clients_name

    @classmethod
    def get__materials_name(cls):
        return cls().__materials_name

    @classmethod
    def db_connect(cls, host, port, user, password, database, charset):
        return pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    def __fetch_content(self, directory, clients, materials):
        # input clients and materials name
        clients_file_name = "clients_name.txt"
        self.__tag_input(clients_file_name, directory, Interpolation.__clients_name)
        materials_file_name = "materials_name.txt"
        self.__tag_input(materials_file_name, directory, Interpolation.__materials_name)
        # input min_date and max_date
        min_date_name = "min_date.txt"
        self.__tag_input(min_date_name, directory, Interpolation.__min_date)
        Interpolation.__min_time = self.__timestamp_transfer(Interpolation.__min_date[0].strip())
        max_date_name = "max_date.txt"
        self.__tag_input(max_date_name, directory, Interpolation.__max_date)
        Interpolation.__max_time = self.__timestamp_transfer(Interpolation.__max_date[0].strip())

        # choose designated files
        file_name = "client-" + clients + "-material-" + str(materials) + ".csv"
        # get dates info
        self.__data_input(file_name, directory, Interpolation.__dates, 1)
        for index, items in enumerate(Interpolation.__dates):
            Interpolation.__dates[index] = self.__timestamp_transfer(items)
            Interpolation.__dates_series.append((Interpolation.__dates[index]
                                                 - Interpolation.__min_time) / Interpolation.__DAY_TIME)
        # get orders info
        self.__data_input(file_name, dat_dir, Interpolation.__orders, 3)

    def __interpolation(self, dates):
        date_no = (self.__timestamp_transfer(dates) - Interpolation.__min_time) / Interpolation.__DAY_TIME
        max_index = (Interpolation.__dates[-1] - Interpolation.__min_time) / Interpolation.__DAY_TIME

        max_index = int(max_index)
        orders = 0
        if date_no < 1:
            orders = self.__inter_method(Interpolation.__dates_series[0],
                                         Interpolation.__dates_series[1],
                                         date_no, 1)
        elif date_no > max_index:
            orders = self.__inter_method(Interpolation.__dates_series[max_index-1],
                                         Interpolation.__dates_series[max_index],
                                         date_no, max_index)
        else:
            for index, num in enumerate(Interpolation.__dates_series):
                if date_no == num:
                    orders = Interpolation.__orders[index]
                elif num < date_no < Interpolation.__dates_series[index + 1]:
                    orders = self.__inter_method(Interpolation.__dates_series[index],
                                                 Interpolation.__dates_series[index+1],
                                                 date_no, index+1)
                else:
                    continue
        return orders

    def __inter_method(self, first_num, second_num, pred_pos, cur_pos):
        res = second_num - (cur_pos - pred_pos)*(second_num - first_num)/2
        if res > 0:
            return res
        else:
            return 0

    def __timestamp_transfer(self, ori_time):
        # dates format: YYYY/mm/dd
        return time.mktime(time.strptime(ori_time, "%Y/%m/%d"))

    def __tag_input(self, file_name, directory, structure):
        """
        :param file_name: name of input file
        :param directory: name of data directory
        :param structure: name of list that data are to stored
        :return: None
        """
        file_path = os.path.join(directory, file_name)
        file = open(file_path, "r", encoding="utf-8", newline="")
        for lines in file:
            structure.append(lines)
        file.close()

    def __data_input(self, file_name, directory, structure, pos):
        """
        :param file_name: name of input file
        :param directory: name of data directory
        :param structure: name of list that data are to stored
        :param pos: 0-pri_key; 1-dates; 2-clients; 3-orders; 4-materials
        :return: None
        """
        file_path = os.path.join(directory, file_name)
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for lines in islice(reader, 1, None):
                structure.append(lines[pos])

    @classmethod
    def data_interpolation(cls, dat_dir, alg_dat_dir, clients, materials, dates):
        """
        step1: define max time and min time in sec
        step2: input data and tags
        """
        # get all possible inputs
        cls().__fetch_content(dat_dir, clients, materials)
        # def interpolation(dates, orders):
        return cls().__interpolation(dates)


if __name__ == "__main__":
    base = os.path.dirname(os.getcwd())
    dat_name = "dat"
    alg_name = "alg_dat"
    dat_dir = os.path.join(base, dat_name)
    alg_dat_dir = os.path.join(base, alg_name)

    clients = "c1"
    materials = 12320670
    dates = "2020/01/15"
    print(Interpolation.data_interpolation(dat_dir, alg_dat_dir, clients, materials, dates))
