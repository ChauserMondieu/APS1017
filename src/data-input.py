import numpy as np
import csv
import os


# import data from
def data_import(date, client, order_quantity, material, dir):
    csv_file = open(dir)
    csv_reader = csv.reader(csv_file)

    # date | client | order quantity | material
    for line in csv_reader:
        date.append(line[0])
        client.append(line[1])
        order_quantity.append(line[2])
        material.append(line[3])
    return date,client,order_quantity,material


if __name__ == "__main__":
    base = os.path.dirname(os.getcwd())
    dat_name = r"dat\APS1017 Order data for Project.csv"
    dir = os.path.join(base, dat_name)

    date = []
    client = []
    order_quantity = []
    material = []
    data_import(date, client, order_quantity, material, dir)
    order_quantity_np = np.array(order_quantity)

