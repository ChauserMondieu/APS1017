import os
import time
import csv
from itertools import islice


class DataInput(object):
    base = os.getcwd()
    dat_name = "dat"
    alg_name = "alg_dat"
    dat_dir = os.path.join(base, dat_name)
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
    def get__min_time(cls):
        return cls().__min_time

    @classmethod
    def get__max_time(cls):
        return cls().__max_time

    @classmethod
    def get__DAY_TIME(cls):
        return cls().__DAY_TIME

    @classmethod
    def fetch_info(cls, directory):
        # input clients and materials name
        clients_file_name = "clients_name.txt"
        cls().__tag_input(clients_file_name, directory, DataInput.__clients_name)
        materials_file_name = "materials_name.txt"
        cls().__tag_input(materials_file_name, directory, DataInput.__materials_name)
        # input min_date and max_date
        min_date_name = "min_date.txt"
        cls().__tag_input(min_date_name, directory, DataInput.__min_date)
        DataInput.__min_time = cls().__timestamp_transfer(DataInput.__min_date[0].strip())
        max_date_name = "max_date.txt"
        cls().__tag_input(max_date_name, directory, DataInput.__max_date)
        DataInput.__max_time = cls().__timestamp_transfer(DataInput.__max_date[0].strip())

    @classmethod
    def fetch_content(cls, directory, clients, materials):
        # choose designated files
        file_name = "client-" + clients + "-material-" + str(materials) + ".csv"
        # get dates info
        cls().__data_input(file_name, directory, DataInput.__dates, 1)
        for index, items in enumerate(DataInput.__dates):
            DataInput.__dates[index] = cls().__timestamp_transfer(items)
            DataInput.__dates_series.append((DataInput.__dates[index]
                                             - DataInput.__min_time) / DataInput.__DAY_TIME)
        # get orders info
        cls().__data_input(file_name, directory, DataInput.__orders, 3)

    @classmethod
    def clear_memo(cls):
        # list for algorithm data: dates, orders
        DataInput.__dates = []
        DataInput.__dates_series = []
        DataInput.__orders = []
        # list for tages
        DataInput.__clients_name = []
        DataInput.__materials_name = []
        # min and max date
        DataInput.__min_date = []
        DataInput.__max_date = []

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





