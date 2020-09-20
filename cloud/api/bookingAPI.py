"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Blueprint, request
from database import Database
from flask.json import jsonify

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/create", methods=['GET', 'POST'])
def create():
    try:
        Database.insert_record_parameterized(
            "Bookings(CustomerID, CarID, RentTime, ReturnTime, TotalCost, Status)",
            "(%s, %s, %s, %s, %s, %s)",
            (
                request.args.get("customer_id"),
                request.args.get("car_id"),
                request.args.get("rent_time"),
                request.args.get("return_time"),
                request.args.get("total_cost"),
                "Booked",
            )
        )
        return "Success"
    except:
        return "Fail"

@booking_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            " Bookings ", 
            " Status = %s",
            " WHERE ID = (%s)",
            (request.args.get("status"), request.args.get("id"))
        ) 
        return "Success"
    except:
        return "Fail"

@booking_api.route("/add/eventId", methods=['GET', 'PUT'])
def add_calendar_booking():
    try:
        Database.update_record_parameterized(
            " Bookings ",
            " EventID = %s ",
            " WHERE ID = (%s)",
            (request.args.get("event_id"), request.args.get("id"))
        )
        return "Success"
    except:
        return "Fail"

@booking_api.route("/cancel/passed/return/time", methods=['GET', 'PUT'])
def update_passed_bookings():
    try:
        Database.update_record_parameterized(
            " Bookings ", 
            " Status = 'Cancelled'",
            " WHERE Status = 'Booked' AND CustomerID = (%s) AND ReturnTime <= NOW()",
            (request.args.get("customer_id"))
        ) 
        return "Success"
    except:
        return "Fail"

@booking_api.route("/read/lastest/record")
def read_last_record():
    results = Database.select_record_parameterized(
        " * ", 
        " Bookings ", 
        " WHERE CarID = %(car_id)s " +
        " AND CustomerID = %(customer_id)s " +
        " AND RentTime = %(rent_time)s " + 
        " AND Status LIKE 'Booked' " +
        " LIMIT 1 ",
        {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id"),
            "rent_time": request.args.get("rent_time")
        },
    ) 
    return jsonify(results)

@booking_api.route("/read/record")
def read_record():
    results = Database.select_record_parameterized(
        " * ", 
        " Bookings ", 
        " WHERE ID = %s ",
        (request.args.get("id"),)
    ) 
    return jsonify(results)

@booking_api.route("/read")
def read():
    results = Database.select_record_parameterized(
        " * ", 
        " Bookings ", 
        " WHERE CarID = %(car_id)s " +
        " AND CustomerID = %(customer_id)s " +
        " AND RentTime <= NOW() AND NOW() <= ReturnTime AND Status = 'Booked' OR Status = 'In use'",
        {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id"),
            "rent_time": request.args.get("rent_time")
        },
    ) 
    return jsonify(results)
    
@booking_api.route("/get/profit/data")
def get_profit_data():
    results = Database.select_record(
        " DATE_FORMAT(RentTime, '%Y-%m-%d') AS Date, CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY Date"
    ) 
    return jsonify(results)

@booking_api.route("/get/most/profit")
def get_most_profit():
    results = Database.select_record_parameterized(
        " CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY DATE(RentTime) ORDER BY Total DESC LIMIT 1",
        ()
    ) 
    return str(results[0]["Total"])

@booking_api.route("/get/data")
def get_bookings_data():
    results = Database.select_record_parameterized(
        " CarID, CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY CarID ORDER BY Total DESC LIMIT 10",
        ()
    ) 
    return jsonify(results)

@booking_api.route("/get/longest/duration")
def get_longest_duration():
    results = Database.select_record_parameterized(
        " CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY CarID ORDER BY Total DESC LIMIT 1",
        ()
    ) 
    return str(results[0]["Total"])

@booking_api.route("/get/all")
def get_all_customer_bookings():
    results = Database.select_record_parameterized(
        " Bookings.RentTime, Bookings.ReturnTime, Bookings.TotalCost, " + 
        " Bookings.Status, Bookings.ID AS BookingID, " +
        " Cars.Brand As CarBrand, Cars.ID AS CarID " , 
        " Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID ", 
        " WHERE CarID = %(car_id)s " +
        " OR CustomerID = %(customer_id)s ",
         {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id")
        }
    )
    return jsonify(results)

@booking_api.route("/get/by/time")
def get_customer_bookings_by_time():
    results = Database.select_record_parameterized(
        " Bookings.RentTime, Bookings.ReturnTime, Bookings.TotalCost, " + 
        " Bookings.Status, Bookings.ID AS BookingID, " +
        " Cars.Brand As CarBrand, Cars.ID AS CarID ", 
        " Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID ", 
        " WHERE CarID = %(car_id)s " +
        " OR CustomerID = %(customer_id)s " +
        " AND RentTime >= %(start)s AND ReturnTime <= %(end)s ",
         {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id"), 
            "start": request.args.get("start"), 
            "end": request.args.get("end")
        }
    )
    return jsonify(results)

@booking_api.route("remove/customer", methods=['GET', 'PUT'])
def remove_customer_from_bookings():
    try:
        Database.update_record_parameterized(
            " Bookings ", 
            " CustomerID = NULL",
            " WHERE CustomerID = (%s)",
            (request.args.get("customer_id"),)
        ) 
        return "Success"
    except:
        return "Fail"

@booking_api.route("remove/car", methods=['GET', 'PUT'])
def remove_car_from_bookings():
    try:
        Database.update_record_parameterized(
            " Bookings ", 
            " CarID = NULL",
            " WHERE CarID = (%s)",
            (request.args.get("car_id"),)
        ) 
        return "Success"
    except:
        return "Fail"
