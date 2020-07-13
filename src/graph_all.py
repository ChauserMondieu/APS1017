import pymysql
from src.graph_plot import *

conn = pymysql.connect(host="192.168.5.12",
                       port=3306,
                       user="develop",
                       password="APS1017s",
                       db="aps1017",
                       charset="utf8")
check_all = "select dates, sum(orders) from aps1017.order_data " \
            "group by dates order by dates;"
cursor = conn.cursor()
cursor.execute(check_all)
result = cursor.fetchall()
order_list = []
date_list = []
for items in result:
    date_list.append(items[0])
    order_list.append(items[1])
print(date_list)
xs = [datetime.strptime(d, '%Y/%m/%d').date() for d in date_list]
num_orders = [int(o) for o in order_list]
np_orders = np.array(num_orders)
max = np_orders.max(axis=0)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line1, = ax.plot(xs, np_orders)
line1.set_label('History orders')
legend = ax.legend(loc='upper right', title='legend')
for i, label in enumerate(np_orders):
    ax.annotate(label, xy=(xs[i], np_orders[i]), rotation=45, fontsize=4)
ax.set_title('History order for all clients and materials')
ax.set_xlabel('Dates', fontsize=8)
ax.set_ylabel('Orders')
ax.set_ylim((0, max+10000))
ax.yaxis.set_major_locator(MultipleLocator(round(max/10)))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_minor_locator(MultipleLocator(round(max/20)))
plt.xticks(rotation=45, fontsize=8)
plt.yticks(rotation=45, fontsize=10)
ax.grid(True)
file_name_ext = "all clients and materials.png"
plt.savefig(os.path.join(GraphPlot.graph_dir, file_name_ext), dpi=400, facecolor='w', edgecolor='w',
            bbox_inches='tight')
plt.close()

