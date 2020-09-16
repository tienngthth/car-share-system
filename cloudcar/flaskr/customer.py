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
from flaskr.script.model.car import Car
from flaskr.script.model.googleCalendar import GoogleCalendar
from flaskr.script.model.booking import Booking
from datetime import *
from datetime import datetime
import requests
import webbrowser
import math
import re
import json
import os

customer = Blueprint("customer", __name__)

@customer.route("/cars", methods=("GET", "POST"))
@login_required
def car_view():
    """Search car by filter"""
    if request.method == "POST":
        return search_car()
    """Display no car"""
    if request.method == "GET":
        return display_no_car()
        
def display_no_car():
    form = UserCarSearchForm()
    return render_template("/customer/car_view.html", cars=[], form=form, start_date="", end_date="")

def search_car():
    form = UserCarSearchForm()
    brand = request.form['brand']
    car_type = request.form['car_type']
    color = request.form['color']
    seat = request.form['seat']
    cost = request.form['cost']
    start_date = datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
    validate_result = Booking.validate_booking_input(cost, start_date, end_date)
    if validate_result != "Valid":
        flash(validate_result)
        return display_no_car()
    cars = requests.get(
        "http://127.0.0.1:8080/cars/get/available/car?brand={}&car_type={}&status=Available&color={}&seat={}&cost={}&start={}&end={}"
        .format(brand, car_type, color, seat, cost, start_date, end_date)).json()["car"]
    return render_template("customer/car_view.html", cars=cars, form=form, start_date=start_date, end_date=end_date)

@customer.route("/book/car", methods=("GET", "POST"))
@login_required
def book_car():
    """Full booking detail"""
    if g.type != "Customer":
        return "Access Denied"
    try:
        car = json.loads(request.args['car'].replace("'", "\""))
        start_date = datetime.strptime(request.args['start_date'], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.args['end_date'], '%Y-%m-%d %H:%M:%S')
    except: 
        return "Missing start_date, end_date or car arguments"
    total_cost = math.ceil((end_date - start_date).total_seconds()/3600) * car['Cost']
    action = "confirm"
    return render_template("customer/booking_detail.html", car=car,start_date=start_date,end_date=end_date, total_cost=total_cost,action=action)

@customer.route("/confirm/booking", methods=("GET", "POST"))
@login_required
def confirm_booking():
    if g.type != "Customer":
        return "Access Denied"
    try:
        car_id = request.args['car_id']
        start_date = datetime.strptime(request.args['start_date'], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.args['end_date'], '%Y-%m-%d %H:%M:%S')
        total_cost = request.args['total_cost']
    except: 
        return "Missing start_date, end_date, car or total cost arguments"
    requests.post("http://127.0.0.1:8080/bookings/create?customer_id={}&car_id={}&rent_time={}&return_time={}&total_cost={}"
    .format(g.user['ID'], car_id, start_date, end_date, total_cost))
    flash("Booking confirmed!")
    create_calendar_event(start_date)
    return redirect(url_for("customer.booking_view"))

def create_calendar_event(start_date):
    # calendar = GoogleCalendar(g.user['Username'])
    # date = datetime.strptime(start_date, '%Y-%m-%d')
    # time = datetime.strptime(start_date, '%H')
    # calendar.insert_event(date, time)
    calendar = GoogleCalendar("abc")
    return caledar.link
    return webbrowser.open_new_tab(calendar.link)
    calendar.insert_event("2020-09-03", "10")

@customer.route("/bookings", methods=("GET", "POST"))
@login_required
def booking_view():
    if g.type != "Customer":
        return "Access Denied"
    form = UserBookingSearchForm()
    if request.method == "POST":
        return filter_booking(form)
    if request.method == "GET":
        return display_all_bookings(form)

def filter_booking(form):
    start_date = datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
    date_validation = Booking.validate_date(start_date, end_date)
    if date_validation != "Valid":
        flash(date_validation)
        return display_all_bookings(form)
    else:
        return display_match_bookings(start_date, end_date, form)
        
def display_match_bookings(start_date, end_date, form):
    user_id = g.user['ID']
    bookings = requests.get(
        "http://127.0.0.1:8080/bookings/get/by/time?customer_id={}&start={}&end={}"
        .format(user_id, start_date, end_date)
    ).json()["bookings"]
    return render_template("customer/booking_view.html", bookings=bookings, form=form)

def display_all_bookings(form):
    user_id = g.user['ID']
    bookings = requests.get(
        "http://127.0.0.1:8080/bookings/get/all?customer_id=" + str(user_id)
    ).json()["bookings"]
    return render_template("customer/booking_view.html", bookings=bookings, form=form)

@customer.route("/bookings/details", methods=("GET", "POST"))
@login_required
def view_booking_detail():
    action = "view"
    booking = json.loads(request.args['booking'].replace("'", "\""))
    start_date = booking["RentTime"]
    end_date = booking["ReturnTime"]
    total_cost = booking["TotalCost"]
    car = requests.get("http://127.0.0.1:8080/cars/get?id=" + str(booking['CarID'])).json()["car"][0]
    status = booking["Status"]
    booking_id=booking["BookingID"]
    return render_template(
        "customer/booking_detail.html", 
        car=car,start_date=start_date,
        end_date=end_date, total_cost=total_cost,
        status=status,booking_id=booking_id,action=action
    )

#Cancel booking (Can only be done by customer)    
@customer.route("/bookings/cancel", methods=("GET", "POST"))
@login_required
def cancel_booking():
    if g.type != "Customer":
        return "Access Denied"
    booking_id = request.args["booking_id"]
    requests.put("http://127.0.0.1:8080/bookings/update?status=Cancelled&id=" + str(booking_id))
    flash("Booking cancelled!")
    return redirect(url_for("customer.booking_view"))