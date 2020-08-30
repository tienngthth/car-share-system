"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Flask
from customerAPI import customer_api
from staffAPI import staff_api
from carAPI import car_api
from bookingAPI import booking_api
from backlogAPI import backlog_api

app = Flask(__name__)

app.register_blueprint(customer_api, url_prefix="/customers")
app.register_blueprint(staff_api, url_prefix="/staffs")
app.register_blueprint(car_api, url_prefix="/cars")
app.register_blueprint(booking_api, url_prefix="/bookings")
app.register_blueprint(backlog_api, url_prefix="/backlogs")

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found"

if __name__ == "__main__":
    app.run(debug=True, port=8080)