from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap

from src.InterpolationAlg import *
from src.DataInput import *
from formClass import Forms

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "APS1017"


@app.route('/', methods=["POST", "GET"])
def index():
    form = Forms.DataQueryForm()
    if request.method == "POST":
        dp = DataInput()
        ia = Interpolation()
        f_clients = request.form.get('clients').strip()
        f_materials = request.form.get('materials').strip()
        f_method = request.form.get('method')
        f_dates = request.form.get('dates')
        form.dates.data = ""
        dp.fetch_content(DataInput.dat_dir, f_clients, f_materials)
        if f_method == "m1":
            orders = ia.data_interpolation(f_dates)
            print(dp.get__dates_series())
        else:
            orders = 0
        dp.clear_memo()
        return redirect(url_for('result', orders=orders))
    return render_template("index.html", form=form)


@app.route('/result/<orders>', methods=["GET"])
def result(orders):
    return render_template("result.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)

