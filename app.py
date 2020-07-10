from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

from src.InterpolationAlg import *
from .formClass import Forms

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "APS1017"


@app.route('/', methods=["POST", "GET"])
def index():
    form = Forms.DataQueryForm()

    if request.method == "POST":
        if form.validate_on_submit() is True:
            return render_template("index.html", form=form)
        else:
            print(form.clients.data)
            f_clients = request.form.get('clients').strip()
            print(f_clients)
            f_materials = form.materials.data.strip()
            f_dates = form.dates.data
            DataInput.fetch_content(Forms.DataQueryForm.dat_dir, f_clients, f_materials)
            f_method = form.method.data
            if f_method == "m1":
                orders = Interpolation.data_interpolation(f_dates)
            else:
                orders = 0
            return render_template("result.html", orders=orders)
    elif request.method == "GET":
        return render_template("index.html", form=form)


@app.route('/result', methods=["GET"])
def result(orders):
    return render_template("result.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)

