#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bookingAPI.py defines the backlog API, whcih handles requests for engineers to repair cars.
"""
from flask import Blueprint, request
from database import Database
from flask.json import jsonify

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/create", methods=['GET', 'POST'])
def create():
    """
    This function creates a new booking. Parameters:
    
    customer_id: The ID of the customer making the booking
    car_id: the ID of the car being booked
    rent_time: The datetime where the user will start renting the car
    return_time: The datetime where the user is supposed to return the car
    total_cost: The expected total invoice for the rental during this period
    
    The function returns Success if a new record is created, and Fail otherwise.
    """
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
    """
    Updates the status of a booking, e.g. to indicate the customer has unlocked the car. Parameters:
    
    status: The new status for the booking
    
    Returns Success if a record was updated, and Fail otherwise.
    """
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
    """
    Update the booking with the calendar ID.
    """
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
    """
    Cancell of the booking that were in the the pass. No parameteres required.
    """
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
    """
    Returns the last booking that the user has just booked, in order to save the calendar id back to the record. Parameters:
    
    car_id: the car id
    customer_id: the customer id
    rent_time: rent_time
    """
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
    """
    Returns a booking by id. Parameters:
    
    id: the booking id
    """
    results = Database.select_record_parameterized(
        " * ", 
        " Bookings ", 
        " WHERE ID = %s ",
        (request.args.get("id"),)
    ) 
    return jsonify(results)

@booking_api.route("/read")
def read():
    """
    Returns any bookings for a given car and user that should be active presently, e.g. where the customer is presently in the car. Parameters:
    
    car_id: The car in question
    customer_id: the customer in question
    
    Returns a dictionary of bookings. The results can be empty.
    """
    results = Database.select_record_parameterized(
        " * ", 
        " Bookings ", 
        " WHERE CarID = %(car_id)s " +
        " AND CustomerID = %(customer_id)s " +
        " AND RentTime <= DATE_ADD(NOW(), INTERVAL 7 HOUR) AND DATE_ADD(NOW(), INTERVAL 7 HOUR) <= ReturnTime AND (Status = 'Booked' OR Status = 'In use')",
        {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id")
        },
    ) 
    return jsonify(results)
    
@booking_api.route("/get/profit/data")
def get_profit_data():
    """
    Returns the profit data by date.
    """
    results = Database.select_record(
        " DATE_FORMAT(RentTime, '%Y-%m-%d') AS Date, CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY Date"
    ) 
    return jsonify(results)

@booking_api.route("/get/most/profit")
def get_most_profit():
    """
    Returns the most profitable car by day as a list. No parameters required. 
    """
    results = Database.select_record_parameterized(
        " CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY DATE(RentTime) ORDER BY Total DESC LIMIT 1",
        ()
    ) 
    return str(results[0]["Total"])

@booking_api.route("/get/data")
def get_bookings_data():
    """
    Returns the profit data by car id
    """
    results = Database.select_record_parameterized(
        " CarID, CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked'  AND CarID != 'None' GROUP BY CarID ORDER BY Total DESC LIMIT 10",
        ()
    ) 
    return jsonify(results)

@booking_api.route("/get/longest/duration")
def get_longest_duration():
    """
    Return a list of the longest signle booking for each car, organized by car. No parameters required.
    """
    results = Database.select_record_parameterized(
        " CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY CarID ORDER BY Total DESC LIMIT 1",
        ()
    ) 
    return str(results[0]["Total"])

@booking_api.route("/get/all")
def get_all_customer_bookings():
    """
    Returns a dictionary of all bookings for a given customer and car. Parameters:
    
    car_id: The car in question
    customer_id: The customer in question
    """
    results = Database.select_record_parameterized(
        " Bookings.RentTime, Bookings.ReturnTime, Bookings.TotalCost, " + 
        " Bookings.Status, Bookings.ID AS BookingID, " +
        " Cars.Brand As CarBrand, Cars.ID AS CarID " , 
        " Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID ", 
        " WHERE CarID = %(car_id)s " +
        " OR CustomerID = %(customer_id)s ORDER BY Bookings.RentTime DESC",
         {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id")
        }
    )
    return jsonify(results)

@booking_api.route("/get/by/time")
def get_customer_bookings_by_time():
    """
    Returns a dictionary of all bookings for a given customer and car, for a given time period. Parameters:
    
    car_id: The car in question
    customer_id: The customer in question
    start: The datetime to start the search period
    end: the datetime to end the search period
    """
    results = Database.select_record_parameterized(
        " Bookings.RentTime, Bookings.ReturnTime, Bookings.TotalCost, " + 
        " Bookings.Status, Bookings.ID AS BookingID, " +
        " Cars.Brand As CarBrand, Cars.ID AS CarID ", 
        " Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID ", 
        " WHERE CarID = %(car_id)s " +
        " OR CustomerID = %(customer_id)s " +
        " AND RentTime >= %(start)s AND ReturnTime <= %(end)s ORDER BY Bookings.RentTime DESC",
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
    """
    Removes a customer from all bookings. Parameters:
    
    customer_id: The customer in question
    
    Returns Success if any records were changed, and Fail otherwise.
    """
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
    """
    Removes a car from all bookings. Parameters:
    
    car_id: The car in question
    
    Returns Success if any records were changed, and Fail otherwise.
    """
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
