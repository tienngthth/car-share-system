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
from flask import Blueprint, Flask, Markup, render_template
import requests

manager = Blueprint("manager", __name__)

@manager.route("/dashboard", methods=("GET",))
def manager_dashboard():
    if g.type != "Manager":
        return redirect(url_for("home.index"))
    if request.method == "GET":
        return render_template("manager/manager_dashboard.html")

@manager.route("/bar_chart", methods=("GET",))
def bar_chart():
    data = requests.get("http://127.0.0.1:8080/bookings/get/data").json()
    max_value = requests.get("http://127.0.0.1:8080/bookings/get/longest/duration").json()["Total"]
    return render_template('manager/bar_chart.html', title='Most booked cars in minutes', max=max_value, data=data["results"])

@manager.route("/line_chart", methods=("GET", "POST"))
def line_chart():
    data = requests.get("http://127.0.0.1:8080/bookings/get/profit/data").json()
    max_value = requests.get("http://127.0.0.1:8080/bookings/get/most/profit").json()["Total"]
    return render_template('manager/line_chart.html', title='Profit by date', max=max_value, data=data["results"])

@manager.route("/pie_chart", methods=("GET",))
def pie_chart():
    pie_colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    data = requests.get("http://127.0.0.1:8080/backlogs/get/backlogs/data").json()
    return render_template('manager/pie_chart.html', title='Most repaired cars', max=20, set=zip(data["results"], pie_colors))