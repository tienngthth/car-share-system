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

customer = Blueprint("customer", __name__)


@customer.route("/bookings", methods=("GET", "POST"))
@login_required
def bookings():
    user = g.user['id']
    form = bookingSearch()
    db = get_db()
    if request.method == "POST":
        bookings = []
        error = None
        try:
            start = request.form['start']
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        except: return "Start date required"
        try:
           end = request.form['end']
           end = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        except: return "End date required"
        if (end - start).days < 0:
            error = "End date must be later than start date"
            return render_template("blog/bookings.html", bookings=bookings, form=form)
        if error is not None:
            flash(error)
        else:   
            bookings = db.execute(
                "SELECT id, Car, User, Created, Starttime, Endtime FROM Booking WHERE User = ? AND Starttime >= ? AND Endtime <= ? ORDER BY Created DESC",(user,start,end,)
            ).fetchall()
        return render_template("blog/bookings.html", bookings=bookings, form=form)

    if request.method == "GET":
        bookings = db.execute(
            "SELECT id, Car, User, Created, Starttime, Endtime FROM Booking WHERE User = ? ORDER BY Created DESC",(user,)).fetchall()
        #do I need these next 2 lines?
        #if form.validate_on_submit():
        #    return redirect(url_for('success'))
        return render_template("blog/bookings.html", bookings=bookings, form=form)


@customer.route("/<int:id>/createbooking", methods=("GET", "POST"))
@login_required
def createbooking(id):
    car = get_car(id)
    user = g.user['id']
    error = None
    try:
        datestart=request.args['datestart']
        datestart = datetime.strptime(datestart, '%Y-%m-%d %H:%M:%S')
    except: return "Start date required"
    try:
        dateend = request.args['dateend']
        dateend = datetime.strptime(dateend, '%Y-%m-%d %H:%M:%S')
    except: return "End date required"
    if (dateend - datestart).days < 0:
        error = "End date must be later than start date"
        form = carSearch()
        datestart = ""
        dateend = ""
        cars = []
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
    if error is not None:
        flash(error)
    else:
        datestart = datestart.strftime("%Y-%m-%d %H:%M")
        dateend = dateend.strftime("%Y-%m-%d %H:%M")
        db = get_db()
        db.execute(
            "INSERT INTO Booking (Car, User, Starttime, Endtime) VALUES (?, ?, ?, ?)",
            (car['id'], user, datestart, dateend),
        )
        db.commit()
        return redirect(url_for("blog.bookings"))




@customer.route("/<int:id>/confirm", methods=("GET", "POST"))
@login_required
def confirm(id):
    """Update a car if the current user is the author."""
    car = get_car(id)
    error = None
    try:
        datestart=request.args['datestart']
        datestart = datetime.strptime(datestart, '%Y-%m-%d %H:%M:%S')
    except: return "Start time required"
    try:
        dateend = request.args['dateend']
        dateend = datetime.strptime(dateend, '%Y-%m-%d %H:%M:%S')
    except: return "End date required"
    if (dateend - datestart).days < 0:
        error = "End date must be later than start date"
        form = carSearch()
        datestart = ""
        dateend = ""
        cars = []
        return render_template("blog/index.html", cars=cars, form=form, datestart=datestart, dateend=dateend)
    if error is not None:
            flash(error)
    else:
        cost = math.ceil((dateend - datestart).total_seconds()/3600) * car['cost']
        return render_template("blog/confirm.html", car=car,datestart=datestart,dateend=dateend, total_cost=cost)



    
    
@customer.route("/<int:id>/calendar", methods=("GET",))
@login_required
def calendar(id):
    user = get_user(g.user['id'])
    booking = get_booking(id)
    # Calendar Sending integration goes here
    #
    #
    return redirect(url_for("blog.index"))
