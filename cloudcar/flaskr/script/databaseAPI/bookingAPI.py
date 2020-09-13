from flask import Blueprint, request
from model.database import Database
from model.util import Util

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

@booking_api.route("/read")
def read():
    results = Database.select_record_parameterized(
        "*", 
        "Bookings", 
        " WHERE CarID = %s " +
        " OR CustomerID = %s ", 
        (request.args.get("car_id"), request.args.get("customer_id"))
    ) 
    return {"results:": Util.paginatedDisplay(results, request.args.get("page"))}

@booking_api.route("/get/profit/data")
def get_all_rent_time():
    results = Database.select_record(
        "DATE(RentTime) AS Date, CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        "Bookings", 
        " WHERE Status = 'Booked' GROUP BY DATE(RentTime)"
    ) 
    return {"results": results}

@booking_api.route("/get/bookings/data")
def get_all_booked_car_ids():
    results = Database.select_record(
        " CarID, CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY CarID"
    ) 
    return {"results": results}

#New APIs start here
@booking_api.route("/get/all/admin/bookings")
def get_all_admin_bookings_for_booking_page():
    results = Database.select_record(
        "Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration," + 
        "Bookings.Status, Bookings.CustomerID, Bookings.ID", 
        "Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID", 
        ""
    )
    return {"booking" : results}

@booking_api.route("/get/admin/booking")
def get_admin_booking_for_admin_booking_page():
    results = Database.select_record_parameterized(
        "Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration," + 
        "Bookings.Status, Bookings.CustomerID, Bookings.ID", 
        "Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID", 
        " WHERE Bookings.RentTime > %s",
        request.args.get("start")
    )
    return {"booking" : results}

@booking_api.route("/get/all/customer/bookings")
def get_all_customer_bookings_for_booking_page():
    results = Database.select_record_parameterized(
        "Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration," +  
        "Bookings.Status, Bookings.ID", 
        "Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID", 
        " WHERE Bookings.CustomerID = %s",
        request.args.get("id")
    )
    return {"booking" : results}

@booking_api.route("/get/customer/booking")
def get_customer_booking_for_admin_booking_page():
    results = Database.select_record_parameterized(
        "Bookings.RentTime, Bookings.CarID, Cars.Brand, Cars.Color, TIMESTAMPDIFF(HOUR,Bookings.RentTime,Bookings.ReturnTime) AS Duration," +
        "Bookings.Status, Bookings.ID", 
        "Cars INNER JOIN Bookings ON Cars.ID = Bookings.CarID", 
        " WHERE Bookings.RentTime > %s AND Bookings.CustomerID = %s",
        (request.args.get("start"), request.args.get("id"))
    )
    return {"booking" : results}

