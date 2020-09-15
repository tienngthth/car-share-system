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

engineer = Blueprint("engineer", __name__)

        
@engineer.route("/engineercars", methods=("GET", "POST"))
@login_required
def engineercars():
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    db = get_db()
    if request.method == "GET":
        cars = db.execute(
            "SELECT id, make, body, colour, seats, location, status, cost, created"
            " FROM Car WHERE status = 'Repair' "
            " ORDER BY created DESC"
        ).fetchall()
        return render_template("blog/engineercars.html", cars=cars)


@engineer.route("/<int:id>/location", methods=("GET", "POST"))
@login_required
def location(id):
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    car = get_car(id)
    db = get_db()
    return render_template("blog/location.html", car=car)

@engineer.route("/<int:id>/fix", methods=("POST",))
@login_required
def fix(id):
    if (g.user['UserType'] != "Engineer"):
        return "Access Denied"
    get_car(id)
    db = get_db()
    db.execute(
            "UPDATE Car SET status = 'Available' WHERE id = ?", (id,)
            )
    db.commit()
    return redirect(url_for("blog.engineercars"))