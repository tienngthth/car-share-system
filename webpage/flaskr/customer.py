"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, url_for, session
from .auth import login_required
from .forms import UserCarSearchForm, UserBookingSearchForm
from googleapiclient.discovery import build
from flaskr.script.model.car import Car
from flaskr.script.model.booking import Booking
from datetime import datetime, timedelta
import requests
import math
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import flask

customer = Blueprint("customer", __name__)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = "https://www.googleapis.com/auth/calendar"
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = "webpage/flaskr/script/files/client_secret.json"

@customer.route("/cars", methods=("GET", "POST"))
@login_required
def car_view():
    if g.type != "Customer":
        return "Access Denied"
    """Customer view car"""
    if (g.type != "Customer"):
        return "Access Denied"
    form = UserCarSearchForm()
    if request.method == "POST":
        return search_car(form)
    if request.method == "GET":
        return display_no_car(form)
        
def display_no_car(form):
    """Display no car"""
    return render_template("/customer/car_view.html", cars=[], form=form, start_date="", end_date="")

def search_car(form):
    """Search available car by filter"""
    brand = request.form['brand']
    car_type = request.form['car_type']
    color = request.form['color']
    seat = request.form['seat']
    cost = request.form['cost']
    start_date = datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
    if not Booking.validate_booking_input(cost, start_date, end_date):
        return display_no_car(form)
    cars = requests.get(
        "http://127.0.0.1:8080/cars/status/available?brand={}&type={}&status=Available&color={}&seat={}&cost={}&start={}&end={}"
        .format(brand, car_type, color, seat, cost, start_date, end_date)
    ).json()
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
    car_id = request.args['car_id']
    start_date = datetime.strptime(request.args['start_date'], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(request.args['end_date'], '%Y-%m-%d %H:%M:%S')
    total_cost = request.args['total_cost']
    requests.post("http://127.0.0.1:8080/bookings/create?customer_id={}&car_id={}&rent_time={}&return_time={}&total_cost={}"
    .format(g.user['ID'], car_id, start_date, end_date, total_cost))
    session["startdate"] = str(start_date.strftime('%Y-%m-%d'))
    session["renttime"] = str(start_date.strftime('%H:%M:%S'))
    endrenttime = start_date + timedelta(minutes = 30)
    session["endrenttime"] = str(endrenttime.strftime('%H:%M:%S'))
    flash("Booking confirmed!") 
    # if request.args["google_calendar"]:
    #     return "Yes"
    #     return redirect(url_for("customer.booking_view"))
    # return "No"
    return redirect(url_for("customer.send_calendar"))
    
@customer.route('/send/calendar', methods=("GET", "POST"))
@login_required
def send_calendar():
    if g.type != "Customer":
        return "Access Denied"
    if 'credentials' not in flask.session:
        return redirect(url_for("customer.authorize"))
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])
    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)
    insert_event(service)
    session['startdate'] = None
    session['renttime'] = None
    session['endrenttime'] = None
    return redirect(url_for("customer.booking_view"))

def insert_event(service):
    event = {
        "summary": "Your car is ready - Car Share",
        "location": "Car Share Office",
        "description": "Please visit Car Share Office to pick up your car",
        "start": {
            "dateTime": "{}T{}+07:00".format(flask.session['startdate'], flask.session['renttime']),
            "timeZone": "Asia/Ho_Chi_Minh",
        },
        "end": {
            "dateTime": "{}T{}+07:00".format(flask.session['startdate'], flask.session['endrenttime']),
            "timeZone": "Asia/Ho_Chi_Minh",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                { "method": "email", "minutes": 5 },
                { "method": "popup", "minutes": 10 },
            ],
        }
    }
    event = service.events().insert(calendarId = "primary", body = event).execute()
    return "send"

@customer.route('/authorize')
@login_required
def authorize():
    if g.type != "Customer":
        return "Access Denied"
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('customer.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    return flask.redirect(authorization_url)

@customer.route('/oauth2callback')
@login_required
def oauth2callback():
    if g.type != "Customer":
        return "Access Denied"
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('customer.oauth2callback', _external=True)
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.redirect(url_for('customer.send_calendar'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

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
    return display_match_bookings(start_date, end_date, form)
        
def display_match_bookings(start_date, end_date, form):
    user_id = g.user['ID']
    bookings = requests.get(
        "http://127.0.0.1:8080/bookings/get/by/time?customer_id={}&start={}&end={}"
        .format(user_id, start_date, end_date)
    ).json()
    return render_template("customer/booking_view.html", bookings=bookings, form=form)

def display_all_bookings(form):
    user_id = g.user['ID']
    bookings = requests.get(
        "http://127.0.0.1:8080/bookings/get/all?customer_id=" + str(user_id)
    ).json()
    return render_template("customer/booking_view.html", bookings=bookings, form=form)

@customer.route("/bookings/details", methods=("GET", "POST"))
@login_required
def view_booking_detail():
    if g.type != "Customer":
        return "Access Denied"
    action = "view"
    booking = json.loads(request.args['booking'].replace("'", "\""))
    start_date = booking["RentTime"]
    end_date = booking["ReturnTime"]
    total_cost = booking["TotalCost"]
    car = requests.get("http://127.0.0.1:8080/cars/read?id=" + str(booking['CarID'])).json()[0]
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