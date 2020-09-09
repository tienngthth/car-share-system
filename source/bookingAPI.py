from flask import Blueprint, request
from model.database import Database

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/get/current/customer/id/by/car/id")
def get_customer_id_by_car_id():
    results = Database.select_record_parameterized(
        "CustomerID", 
        "Bookings", 
        " WHERE CarID = %s" + 
        " AND DATE(RentTime) = CAST(NOW() AS Date)",
        (request.args.get("car_id"))
    )   
    if len(results) == 0:
        return "No customer found"
    else: 
        return str(results[0][0])

@booking_api.route("/get/booking/by/customer/or/car/id")
def get_booking_by_car_or_customer_id():
    results = Database.select_record_parameterized(
        "*", 
        "Bookings", 
        " WHERE CarID = %s" +
        " OR CustomerID = %s", 
        (
            request.args.get("car_id"), 
            request.args.get("customer_id"), 
        )
    ) 
    if len(results) == 0:
        return "No booking found"
    else: 
        return str(results)

@booking_api.route("/get/all/rent/time")
def get_all_rent_time():
    results = Database.select_record(
        "DATE(RentTime) AS Date", 
        "Bookings", 
        " WHERE Status = 'Booked' GROUP BY DATE(RentTime)"
    ) 
    if len(results) == 0:
        return "No rent time found"
    else: 
        return str(results)

@booking_api.route("/get/total/costs/wrt/rent/time")
def get_total_cost_wrt_rent_time():
    results = Database.select_record(
        "SUM(TotalCost) AS Daily_Profit", 
        "Bookings", 
        " WHERE Status = 'Booked' GROUP BY DATE(RentTime)"
    ) 
    if len(results) == 0:
        return "No rent time found"
    else: 
        return str(results)

@booking_api.route("/get/all/booked/car/ids")
def get_all_booked_car_ids():
    results = Database.select_record(
        "CarID", 
        "Bookings", 
        " WHERE Status = 'Booked' GROUP BY CarID"
    ) 
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results)

@booking_api.route("/get/booked/time/wrt/car/id")
def get_booked_time_wrt_car_id():
    results = Database.select_record(
        "SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)) as Booked_time", 
        "Bookings", 
        " WHERE Status = 'Booked' GROUP BY CarID"
    ) 
    if len(results) == 0:
        return "No car found"
    else: 
        return str(results)

@booking_api.route("/create", methods=['GET', 'POST'])
def create_booking():
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
    return "Done"

@booking_api.route("/update/status/by/id", methods=['GET', 'PUT'])
def update_status_by_id():
    Database.update_record_parameterized(
        "Bookings", 
        " Status = %s",
        " WHERE ID = (%s)",
        (request.args.get("status"), request.args.get("id"))
    ) 
    return "Done"