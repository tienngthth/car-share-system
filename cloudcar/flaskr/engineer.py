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
import requests
import os

engineer = Blueprint("engineer", __name__)

@engineer.route("/cars", methods=("GET", "POST"))
@login_required
def car_view():
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    if request.method == "GET":
        backlogs = requests.get("http://127.0.0.1:8080/backlogs/get/all").json()["backlogs"]
        return render_template("engineer/backlog_view.html", backlogs=backlogs)

@engineer.route("/location", methods=("GET", "POST"))
@login_required
def location_map():
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    car = requests.get("http://127.0.0.1:8080/cars/get?id=" + request.args['car_id']).json()["car"][0]
    location = requests.get("http://127.0.0.1:8080/cars/get/location?id=" + request.args['location_id']).json()["location"][0]
    return render_template("engineer/location_map.html", car=car, location=location)

@engineer.route("/close/backlog", methods=("POST",))
@login_required
def close_backlog():
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    requests.put(
        "http://127.0.0.1:8080/backlogs/close?car_id={}&signed_engineer_id={}"
        .format(request.args['car_id'], g.user['ID'])
    )
    requests.put(
        "http://127.0.0.1:8080/cars/update?id={}&status=Available"
        .format(request.args['car_id'])
    )
    return redirect(url_for("engineer.car_view"))