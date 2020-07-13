from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src.DataInput import *


class Forms(object):

    class DataQueryForm(Form):
        # tag preparation
        DataInput.fetch_info(DataInput.dat_dir)
        clients_tags = DataInput.get__clients_name()
        clients_tags.append("all")
        materials_tags = DataInput.get__materials_name()
        materials_tags.append("all")
        # form construction
        clients = SelectField(label="Please choose Client No.:",
                              choices=clients_tags, coerce=str)
        materials = SelectField(label="Please choose Material No.:",
                                choices=materials_tags, coerce=str)
        dates = StringField(label="Please input Date", validators=[DataRequired()], default="YYYY/mm/dd")
        method = SelectField(label="Please choose prediction method:",
                             choices=['ARIMA', 'Moving Average', 'Holt-Winter'], coerce=str)
        submit = SubmitField(label="Submit")