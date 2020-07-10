from src.DataInput import *


class Interpolation(object):
    @classmethod
    def data_interpolation(cls, dates):
        # def interpolation(dates, orders):
        return cls().__interpolation(dates)

    def __interpolation(self, dates):
        date_no = (self.__timestamp_transfer(dates) - DataInput.get__min_time()) / DataInput.get__DAY_TIME()
        max_index = (DataInput.get__dates()[-1] - DataInput.get__min_time()) / DataInput.get__DAY_TIME()

        max_index = int(max_index)
        orders = 0
        if date_no < 1:
            orders = self.__inter_func(DataInput.get__dates_series()[0],
                                       DataInput.get__dates_series()[1],
                                       date_no, 1)
        elif date_no > max_index:
            orders = self.__inter_func(DataInput.get__dates_series()[max_index - 1],
                                       DataInput.get__dates_series()[max_index],
                                       date_no, max_index)
        else:
            for index, num in enumerate(DataInput.get__dates_series()):
                if date_no == num:
                    orders = DataInput.get__orders()[index]
                elif num < date_no < DataInput.get__dates_series()[index + 1]:
                    orders = self.__inter_func(DataInput.get__dates_series()[index],
                                               DataInput.get__dates_series()[index + 1],
                                               date_no, index + 1)
                else:
                    continue
        return orders

    def __inter_func(self, first_num, second_num, pred_pos, cur_pos):
        res = second_num - (cur_pos - pred_pos) * (second_num - first_num) / 2
        if res > 0:
            return res
        else:
            return 0

    def __timestamp_transfer(self, ori_time):
        # dates format: YYYY/mm/dd
        return time.mktime(time.strptime(ori_time, "%Y/%m/%d"))

