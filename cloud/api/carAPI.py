#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, request
from database import Database
from flask.json import jsonify

car_api = Blueprint("car_api", __name__)

@car_api.route("/create", methods=['GET', 'POST'])
def create():
    try:
        Database.insert_record_parameterized(
            "Cars(MacAddress, Brand, Type, LocationID, Status, Color, Seat, Cost) ",
            "(%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                request.args.get("mac_address"),
                request.args.get("brand"),
                request.args.get("type"),
                request.args.get("location_id"),
                request.args.get("status"),
                request.args.get("color"),
                request.args.get("seat"),
                request.args.get("cost"),
            )
        )
        return "Success"
    except:
        return "Fail"

@car_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            " Cars ",
            " MacAddress = CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
            " THEN MacAddress ELSE %(mac_address)s END, " +
            " Brand = CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
            " THEN Brand ELSE %(brand)s END, " +
            " Type = CASE WHEN %(type)s = '' OR %(type)s IS NULL " + 
            " THEN Type ELSE %(type)s END, " +
            " LocationID = CASE WHEN %(location_id)s = '' OR %(location_id)s IS NULL " + 
            " THEN LocationID ELSE %(location_id)s END, " +
            " Status = CASE WHEN %(status)s = '' OR %(status)s IS NULL " + 
            " THEN Status ELSE %(status)s END, " +
            " Color = CASE WHEN %(color)s = '' OR %(color)s IS NULL " + 
            " THEN Color ELSE %(color)s END, " +
            " Seat = CASE WHEN %(seat)s = '' OR %(seat)s IS NULL " + 
            " THEN Seat ELSE %(seat)s END, " +
            " Cost = CASE WHEN %(cost)s = '' OR %(cost)s IS NULL " + 
            " THEN Cost ELSE %(cost)s END ",
            " WHERE ID = %(car_id)s", 
            {
                "car_id": request.args.get("id"),
                "mac_address": request.args.get("mac_address"), 
                "brand": request.args.get("brand"), 
                "type": request.args.get("type"),
                "location_id": request.args.get("location_id"), 
                "status": request.args.get("status"),
                "color": request.args.get("color"),
                "seat": request.args.get("seat"),
                "cost": request.args.get("cost")
            }
        )
        return "Success"
    except:
        return "Fail"

@car_api.route("/delete", methods=['GET', 'DELETE'])
def delete_car():
    try:
        Database.delete_record_parameterized(
            " Cars ",
            " WHERE ID = %s"
            , (request.args.get("id"),)
        )
        return "Success"
    except:
        return "Fail"

@car_api.route("/read")
def read():
    results = Database.select_record_parameterized(
        " Cars.ID, Cars.Brand, Cars.Type, Cars.Color, Cars.MacAddress, " +
        " Cars.Seat, Locations.Address, Cars.Cost, Cars.Status", 
        " Cars INNER JOIN Locations ON Cars.LocationID = Locations.ID ", 
        " WHERE Cars.ID LIKE CASE WHEN %(id)s = '' OR %(id)s IS NULL " +
        " THEN Cars.ID ELSE %(id)s END " +
        " AND MacAddress LIKE CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
        " THEN MacAddress ELSE %(mac_address)s END " +
        " AND Brand LIKE CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
        " THEN Brand ELSE %(brand)s END " +
        " AND Type LIKE CASE WHEN %(type)s = '' OR %(type)s IS NULL " +
        " THEN Type ELSE %(type)s END " +
        " AND Status LIKE CASE WHEN %(status)s = '' OR %(status)s IS NULL " +
        " THEN Status ELSE %(status)s END " +
        " AND Color LIKE CASE WHEN %(color)s = '' OR %(color)s IS NULL " +
        " THEN Color ELSE %(color)s END " +
        " AND Seat LIKE CASE WHEN %(seat)s = '' OR %(seat)s IS NULL " +
        " THEN Seat ELSE %(seat)s END " +
        " AND Cost <= CASE WHEN %(cost)s = '' OR %(cost)s IS NULL " +
        " THEN Cost ELSE %(cost)s END ",
        {
            "id": request.args.get("id"), 
            "mac_address": request.args.get("mac_address"), 
            "brand": request.args.get("brand"), 
            "type": request.args.get("type"), 
            "status": request.args.get("status"), 
            "color": request.args.get("color"), 
            "seat": request.args.get("seat"), 
            "cost": request.args.get("cost")
        }
    ) 
    return jsonify(results)

@car_api.route("/status/available")
def get_available_car():
    results = Database.select_record_parameterized(
        " Cars.ID, Cars.Brand, Cars.Type, Cars.Color, Cars.MacAddress, " +
        " Cars.Seat, Locations.Address, Cars.Cost, Cars.Status",
        " Cars INNER JOIN Locations ON Cars.LocationID = Locations.ID ", 
        " WHERE MacAddress LIKE CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
        " THEN MacAddress ELSE %(mac_address)s END " +
        " AND Brand LIKE CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
        " THEN Brand ELSE %(brand)s END " +
        " AND Type LIKE CASE WHEN %(type)s = '' OR %(type)s IS NULL " +
        " THEN Type ELSE %(type)s END " +
        " AND Cars.Status LIKE 'Available' " +
        " AND Color LIKE CASE WHEN %(color)s = '' OR %(color)s IS NULL " +
        " THEN Color ELSE %(color)s END " +
        " AND Seat LIKE CASE WHEN %(seat)s = '' OR %(seat)s IS NULL " +
        " THEN Seat ELSE %(seat)s END " +
        " AND Cost <= CASE WHEN %(cost)s = '' OR %(cost)s IS NULL " +
        " THEN Cost ELSE %(cost)s END " +
        " AND Cars.ID NOT IN (SELECT Bookings.CarID AS ID From Bookings " +
        " WHERE Bookings.RentTime <= %(end)s AND Bookings.ReturnTime >= %(start)s AND Bookings.Status NOT LIKE 'Cancelled')",
        {
            "mac_address": request.args.get("mac_address"), 
            "brand": request.args.get("brand"), 
            "type": request.args.get("type"), 
            "color": request.args.get("color"), 
            "seat": request.args.get("seat"), 
            "cost": request.args.get("cost"),
            "start": request.args.get("start"),
            "end": request.args.get("end")
        }
    ) 
    return jsonify(results)

@car_api.route("get/id")
def get_car_id_by_mac_address():
    results = Database.select_record_parameterized(
        " ID ",
        " Cars ",
        " WHERE MacAddress = %s AND MacAddress NOT LIKE ''",
        (request.args.get("mac_address"),)
    )
    if len(results) == 0:
        return "No car found"
    else:
        return str(results[0]["ID"])

@car_api.route("history")
def get_car_history():
    results = Database.select_record_parameterized(
        " Bookings.ID, Bookings.CarID, Bookings.CustomerID, Bookings.RentTime, " +
        " Bookings.ReturnTime, Bookings.TotalCost, Bookings.Status ", 
        " Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID ",
        " WHERE Cars.ID = %s",
        (request.args.get("id"),)
    )
    return jsonify(results)