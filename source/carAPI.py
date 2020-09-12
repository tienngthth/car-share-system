from flask import Blueprint, request
from model.database import Database
from model.util import Util

car_api = Blueprint("car_api", __name__)

@car_api.route("/create", methods=['GET', 'POST'])
def create():
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
    return "Done"

@car_api.route("/read")
def read():
    results = Database.select_record_parameterized(
        "*", 
        "Cars", 
        " WHERE MacAddress LIKE CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
        " THEN MacAddress ELSE %(mac_address)s END " +
        " AND Brand LIKE CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
        " THEN Brand ELSE %(brand)s END " +
        " AND Type LIKE CASE WHEN %(car_type)s = '' OR %(car_type)s IS NULL " +
        " THEN Type ELSE %(car_type)s END " +
        " AND Status LIKE CASE WHEN %(status)s = '' OR %(status)s IS NULL " +
        " THEN Status ELSE %(status)s END " +
        " AND Color LIKE CASE WHEN %(color)s = '' OR %(color)s IS NULL " +
        " THEN Color ELSE %(color)s END " +
        " AND Seat LIKE CASE WHEN %(seat)s = '' OR %(seat)s IS NULL " +
        " THEN Seat ELSE %(seat)s END " +
        " AND Cost LIKE CASE WHEN %(cost)s = '' OR %(cost)s IS NULL " +
        " THEN Cost ELSE %(cost)s END ",
        {
            "mac_address": request.args.get("mac_address"), 
            "brand": request.args.get("brand"), 
            "car_type": request.args.get("car_type"), 
            "status": request.args.get("status"), 
            "color": request.args.get("color"), 
            "seat": request.args.get("seat"), 
            "cost": request.args.get("cost")
        }
    ) 
    return {"results:": Util.paginatedDisplay(results, request.args.get("page"))}

@car_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            "Cars",
            " MacAddress = CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
            " THEN MacAddress ELSE %(mac_address)s END, " +
            " Brand = CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
            " THEN Brand ELSE %(brand)s END, " +
            " Type = CASE WHEN %(car_type)s = '' OR %(car_type)s IS NULL " + 
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
                "car_type": request.args.get("car_type"),
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
            "Cars",
            " WHERE ID = %s"
            , request.args.get("id"),
        )
        return "Success"
    except:
        return "Fail"

@car_api.route("get/car/id/by/mac/address")
def get_car_id_by_mac_address():
    results = Database.select_record_parameterized(
        " ID ",
        " Cars ",
        " WHERE MacAddress = %s ",
        (request.args.get("mac_address"),)
    )
    return {"car_id": results}