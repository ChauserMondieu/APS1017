from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap

from src.InterpolationAlg import *
from src.DataInput import *
from src.ARIMA import *
from formClass import Forms

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "APS1017"
base = os.getcwd()
dat_dir = os.path.join(base, "dat")


@app.route('/', methods=["POST", "GET"])
def index():
    form = Forms.DataQueryForm()
    if request.method == "POST":
        dp = DataInput()
        # ia = Interpolation()
        ar = ARIMA()
        f_clients = request.form.get('clients').strip()
        f_materials = request.form.get('materials').strip()
        f_method = request.form.get('method')
        f_dates = request.form.get('dates')
        print(f_dates, f_clients, f_materials)
        form.dates.data = ""
        # dp.fetch_content(DataInput.dat_dir, f_clients, f_materials)
        if f_method == "ARIMA":
            orders = ar.ARIMA(dat_dir, f_clients, f_materials, f_dates)
            # orders = ia.data_interpolation(f_dates)
        elif f_method == "Moving Average":
            if f_materials != "all" and f_clients != "all":
                return render_template("none_agg_res.html", f_method=f_method)
            else:
                orders = 0
                return redirect(url_for('result', orders=orders))
        elif f_method == "Holt-Winter":
            if f_materials != "all" and f_clients != "all":
                return render_template("none_agg_res.html", f_method=f_method)
            else:
                orders = 0
                return redirect(url_for('result', orders=orders))
        else:
            orders = 0
        dp.clear_memo()
        return redirect(url_for('result', orders=orders))
    return render_template("index.html", form=form)


@app.route('/history', methods=['GET'])
def history_order():
    return render_template("history_order.html")


@app.route('/result/<orders>', methods=["GET"])
def result(orders):
    return render_template("result.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)

