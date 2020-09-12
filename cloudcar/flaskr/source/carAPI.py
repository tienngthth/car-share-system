from flask import Blueprint, request
from model.database import Database
from model.util import Util

car_api = Blueprint("car_api", __name__)

@car_api.route("get/car/latitude/from/backlog")
def get_car_latitude():
    results = Database.select_record_parameterized(
        "Locations.Latitude", 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID", 
        " WHERE Backlogs.ID = %s",
        request.args.get("id")
    )
    if len(results) == 0:
        return "No car found"
    else: 
        return str(Database.get_list_from_tuple_list(results))

@car_api.route("get/car/longitude/from/backlog")
def get_car_longitude():
    results = Database.select_record_parameterized(
        "Locations.Longitude", 
        "Cars INNER JOIN Backlogs ON Cars.ID = Backlogs.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID", 
        " WHERE Backlogs.ID = %s",
        request.args.get("id")
    )
    if len(results) == 0:
        return "No car found"
    else: 
        return str(Database.get_list_from_tuple_list(results))

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
            " Type = CASE WHEN %(type)s = '' OR %(type)s IS NULL " + 
            " THEN Type ELSE %(type)s END, " +
            " LocationID = CASE WHEN %(locationID)s = '' OR %(locationID)s IS NULL " + 
            " THEN LocationID ELSE %(locationID)s END, " +
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
                "locationID": request.args.get("locationID"), 
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

#New API starts from here
@car_api.route("index/get/car")
def get_car_for_index_page():
    results = Database.select_record_parameterized(
        "Cars.ID, Cars.Brand, Cars.Type, Cars.Color, Cars.Seat, Locations.Address, Cars.Cost", 
        "Cars INNER JOIN Locations ON Cars.LocationID = Locations.ID", 
        " WHERE Brand LIKE %s AND Color LIKE %s",
        (request.args.get("brand"), request.args.get("color"))
    )
    return {"car": results}

@car_api.route("admin/search/car")
def get_car_for_admin_page():
    results = Database.select_record_parameterized(
        "Cars.ID, Cars.Type, Cars.Brand, Cars.Color, Locations.Address, Bookings.Status",
        "Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
        " WHERE Cars.Brand LIKE %s AND Cars.Color LIKE %s ORDER BY Bookings.RentTime DESC",
        (request.args.get("brand"), request.args.get("color"))
    )
    return {"car": results}

@car_api.route("admin/get/all/cars")
def get_all_cars_for_admin_page():
    results = Database.select_record(
        "Cars.ID, Cars.Type, Cars.Brand, Cars.Color, Locations.Address, Bookings.Status",
        "Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID INNER JOIN Locations ON Cars.LocationID = Locations.ID",
        " ORDER BY Bookings.RentTime DESC"
    )
    return {"car": results}

@car_api.route("get/car/by/ID")
def get_car_by_ID():
    results = Database.select_record_parameterized(
        "*", 
        "Cars",
        " WHERE Cars.ID = %s",
        request.args.get("id")
    )
    return {"car": results}