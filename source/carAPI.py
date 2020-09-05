from flask import Blueprint, request
from model.database import Database


car_api = Blueprint("car_api", __name__)

@car_api.route("get/car/id/by/mac/address")
def get_car_id_by_mac_address():
    results = Database.select_record_parameterized(
        "ID",
        "Cars",
        " WHERE MacAddress = %s",
        request.args.get("mac_address")
    )
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results[0][0])

@car_api.route("/get/cars/by/filter")
def get_cars_by_filter():
    results = Database.select_record_parameterized(
        "*", 
        "Cars", 
        " WHERE MacAddress LIKE %s" +
        " AND Brand LIKE %s" +
        " AND Type LIKE %s" +
        " AND Latitude LIKE %s " +
        " AND Longtitude LIKE %s " +
        " AND Status LIKE %s" + 
        " AND Color LIKE %s" +
        " AND Seat LIKE %s" +
        " AND Cost LIKE %s", 
        (
            "%{}%".format(request.args.get("mac_address")), 
            "%{}%".format(request.args.get("brand")), 
            "%{}%".format(request.args.get("car_type")), 
            "%{}%".format(request.args.get("latitude")),
            "%{}%".format(request.args.get("longtitude")),  
            "%{}%".format(request.args.get("status")), 
            "%{}%".format(request.args.get("color")), 
            "%{}%".format(request.args.get("seat")), 
            "%{}%".format(request.args.get("cost")),
        )
    ) 
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results)

@car_api.route("get/car/latitude/from/backlog")
def get_car_latitude():
    results = Database.select_record_parameterized(
        "Cars.Latitude", 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID", 
        " WHERE Backlogs.ID = %s",
        request.args.get("id")
    )
    if len(results) == 0:
        return "No car found"
    else: 
        return str(Database.get_list_from_tuple_list(results))

@car_api.route("get/car/longtitude/from/backlog")
def get_car_longtitude():
    results = Database.select_record_parameterized(
        "Cars.Longtitude", 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID", 
        " WHERE Backlogs.ID = %s",
        request.args.get("id")
    )
    if len(results) == 0:
        return "No car found"
    else: 
        return str(Database.get_list_from_tuple_list(results))

@car_api.route("/create", methods=['GET', 'POST'])
def create_car():
    Database.insert_record_parameterized(
        "Cars(MacAddress, Brand, Type, Latitude, Longtitude, Status, Color, Seat, Cost) ",
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            request.args.get("mac_address"),
            request.args.get("brand"),
            request.args.get("type"),
            request.args.get("latitude"),
            request.args.get("longtitude"),
            request.args.get("status"),
            request.args.get("color"),
            request.args.get("seat"),
            request.args.get("cost"),
        )
    )
    return "Done"

@car_api.route("/delete", methods=['GET', 'DELETE'])
def delete_car():
    Database.delete_record_parameterized(
        "Cars",
        " WHERE ID = %s"
        , request.args.get("id"),
    )
    return "Done"

@car_api.route("/update", methods=['GET', 'PUT'])
def update_car():
    Database.update_record_parameterized(
        "Cars",
        " MacAddress = CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
        " THEN MacAddress ELSE %(mac_address)s END, " +
        " Brand = CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
        " THEN Brand ELSE %(brand)s END, " +
        " Type = CASE WHEN %(type)s = '' OR %(type)s IS NULL " + 
        " THEN Type ELSE %(type)s END, " +
        " Latitude = CASE WHEN %(latitude)s = '' OR %(latitude)s IS NULL " + 
        " THEN Latitude ELSE %(latitude)s END, " +
        " Longtitude = CASE WHEN %(longtitude)s = '' OR %(longtitude)s IS NULL " + 
        " THEN Longtitude ELSE %(longtitude)s END, " +
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
            "latitude": request.args.get("latitude"), 
            "longtitude": request.args.get("longtitude"), 
            "status": request.args.get("status"),
            "color": request.args.get("color"),
            "seat": request.args.get("seat"),
            "cost": request.args.get("cost")
        }
    )
    return "Done"