from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import numpy as np
from datetime import datetime
from src.DataInput import *


class GraphPlot(object):
    base = os.path.dirname(os.getcwd())
    dat_dir = os.path.join(base, "dat")
    graph_dir = os.path.join(base, "bin")
    # info for file name
    materials_name = list()
    clients_name = list()

    @classmethod
    def filename_loader(cls):
        DataInput.fetch_info(GraphPlot.dat_dir)
        GraphPlot.materials_name = DataInput.get__materials_name()
        GraphPlot.clients_name = DataInput.get__clients_name()

    @classmethod
    def data_loader(cls, path):
        orders = list()
        dates = list()
        for clients in GraphPlot.clients_name:
            for materials in GraphPlot.materials_name:
                file_name = "client-" + clients.strip() + "-material-" + materials.strip()
                file_name_ext = file_name + ".csv"
                file_path = os.path.join(path, file_name_ext)
                with open(file_path, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for lines in islice(reader, 1, None):
                        dates.append(lines[1])
                        orders.append(lines[3])
                GraphPlot.data_plot(clients, materials, orders, dates, file_name)
                print(file_name + ' has successfully plotted')
                # reset
                dates = []
                orders = []

    @classmethod
    def data_plot(cls, clients, materials, orders, dates, file_name):
        xs = [datetime.strptime(d, '%Y/%m/%d').date() for d in dates]
        if len(orders) != 0:
            num_orders = [int(o) for o in orders]
            np_orders = np.array(num_orders)
            max = np_orders.max(axis=0)
        else:
            return True
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        line1, = ax.plot(xs, np_orders)
        line1.set_label('History orders')
        legend = ax.legend(loc='upper right', title='legend')
        for i, label in enumerate(np_orders):
            ax.annotate(label, (xs[i], np_orders[i]), rotation=45, fontsize=4)
        ax.set_title('History order for client {:s} on material {:s}'.format(clients.strip(), materials.strip()))
        ax.set_xlabel('Dates', fontsize=8)
        ax.set_ylabel('Orders')
        ax.set_ylim((0, max+100))
        ax.yaxis.set_major_locator(MultipleLocator(round(max/10)))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.yaxis.set_minor_locator(MultipleLocator(round(max/20)))
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(rotation=45, fontsize=10)
        ax.grid(True)
        file_name_ext = file_name + ".png"
        plt.savefig(os.path.join(GraphPlot.graph_dir, file_name_ext), dpi=400, facecolor='w', edgecolor='w',
                    bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    GraphPlot.filename_loader()
    GraphPlot.data_loader(GraphPlot.dat_dir)
