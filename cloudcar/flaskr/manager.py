from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from .auth import login_required
from .forms import *
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import DateTimeLocalInput
from datetime import *
import math
import re
import os

manager = Blueprint("manager", __name__)

#graph integration
def make_profit_line_chart():
    Database = get_db()
    labels = Database.select_record("DATE(RentTime) AS Date", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    values = Database.select_record("SUM(TotalCost) AS Daily_Profit", "Bookings", " WHERE Status = 'Booked' GROUP BY DATE(RentTime)")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_booked_car_bar_chart():
    Database = get_db()
    labels = Database.select_record("CarID", "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    values = Database.select_record("SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)) as Booked_time", 
    "Bookings", " WHERE Status = 'Booked' GROUP BY CarID")
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values)

def make_backlog_pie_chart():
    Database = get_db()
    labels = Database.select_record("CarID", "Backlogs", " GROUP BY CarID")
    values = Database.select_record("COUNT(CarID) as Number_of_repairs", "Backlogs", " GROUP BY CarID")
    colors = ["#F7464A", "#46BFBD", "#FDB45C"]
    return Database.get_list_from_tuple_list(labels), Database.get_list_from_tuple_list(values), colors


@manager.route("/bar", methods=("GET", "POST"))
@login_required
def bar():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    bar_labels = make_booked_car_bar_chart()[0]
    bar_values = make_booked_car_bar_chart()[1]
    return render_template('bar_chart.html', title='Most booked cars in minutes', max=15000, labels=bar_labels, values=bar_values)

@manager.route("/line", methods=("GET", "POST"))
@login_required
def line():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    line_labels = make_profit_line_chart()[0]
    line_values = make_profit_line_chart()[1]
    return render_template('line_chart.html', title='Profit by date', max=1000, labels=line_labels, values=line_values)

@manager.route("/pie", methods=("GET", "POST"))
@login_required
def pie():
    if (g.user['UserType'] != "Manager"):
        return "Access Denied"
    pie_labels = make_backlog_pie_chart()[0]
    pie_values = make_backlog_pie_chart()[1]
    pie_colors = make_backlog_pie_chart()[2]
    return render_template('pie_chart.html', title='Most repaired cars', max=10, set=zip(pie_values, pie_labels, pie_colors))


@manager.route("/dashboard", methods=("GET", "POST"))
def manager_dashboard():
    if request.method == "GET":
        try:
            graph = request.args["graph"]
        except: graph = "barchart"
        
        if graph == "barchart":
            return render_template("blog/bar_chart.html")
        elif graph == "linechart":
            return render_template("blog/line_chart.html")
        elif graph == "piechart":
            return render_template("blog/pie_chart.html")
        
        else:
            return "No graph of that type."