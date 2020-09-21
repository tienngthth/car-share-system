#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request
from customerAPI import customer_api
from staffAPI import staff_api
from carAPI import car_api
from bookingAPI import booking_api
from backlogAPI import backlog_api
from locationAPI import location_api
from database import Database

app = Flask(__name__)

app.register_blueprint(customer_api, url_prefix="/customers")
app.register_blueprint(staff_api, url_prefix="/staffs")
app.register_blueprint(car_api, url_prefix="/cars")
app.register_blueprint(booking_api, url_prefix="/bookings")
app.register_blueprint(backlog_api, url_prefix="/backlogs")
app.register_blueprint(location_api, url_prefix="/locations")

@app.errorhandler(404)
def page_not_found(e):
    """
    This errorhandler passes the error text defined here whenever a user gets a 404 page not found error
    """
    return "Page not found"

@app.route("/get/user/info")
def get_encrypted_password():
    """
    This returns a user's hashed password.
    """
    username = request.args.get("username")
    user = get_user("Customers", username)
    if len(user) == 0:
        user = get_user("Staffs", username)
        if len(user) == 0:
            return "invalid"
    return user[0]

def get_user(user_type, username):
    """
    This returns a user entry from the database given their name and type. Parameters:
    
    username: The username
    user_type: The user type, e.g. engineer
    """
    return Database.select_record_parameterized(
        " * ", 
        user_type,
        " WHERE Username = %s ", 
        (username,)
    )  

if __name__ == "__main__":
    app.run(debug=True, port=8080)
