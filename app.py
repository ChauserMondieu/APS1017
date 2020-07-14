from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap

# from src.InterpolationAlg import *
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
        ar = Arima()
        f_clients = request.form.get('clients').strip()
        f_materials = request.form.get('materials').strip()
        f_method = request.form.get('method')
        f_dates = request.form.get('dates')
        form.dates.data = ""
        # print(f_clients, f_materials, f_method)
        # dp.fetch_content(DataInput.dat_dir, f_clients, f_materials)
        if f_method == "ARIMA":
            if f_clients == "all" and f_materials == "all":
                return render_template("no_data.html")
            else:
                orders = ar.ARIMA_main(dat_dir, f_clients, f_materials, f_dates)[0]
                prediction_img = ar.ARIMA_main(dat_dir, f_clients, f_materials, f_dates)[1]
                # orders = ia.data_interpolation(f_dates)
                return redirect(url_for('result', orders=orders, f_id=prediction_img))
        dp.clear_memo()
    return render_template("index.html", form=form)


@app.route('/history', methods=['GET'])
def history_order():
    return render_template("history_order.html")


@app.route('/result/<orders>?<f_id>', methods=["GET"])
def result(orders, f_id):
    return render_template("result.html", orders=orders, prediction_img='/static/' + f_id)


if __name__ == "__main__":
    app.run()

