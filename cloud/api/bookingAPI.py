"""
bookingAPI.py defines the backlog API, whcih handles requests for engineers to repair cars.
"""
from flask import Blueprint, request
from database import Database

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
        " OR CustomerID = %(customer_id)s " +
        " AND RentTime <= NOW() AND NOW() <= ReturnTime ",
        {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id")
        }
    ) 
    return {"bookings" : results}

@booking_api.route("/get/profit/data")
def get_all_rent_time():
    """
    Returns the gross profit renting cars as a dictionary, organized by Date. No parameters required.
    """
    results = Database.select_record(
        " DATE_FORMAT(RentTime, '%Y-%m-%d') AS Date, CONVERT(SUM(TotalCost), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY Date"
    ) 
    return {"results": results}

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
    return results[0]

@booking_api.route("/get/data")
def get_all_booked_car_ids():
    """
    Return a dictionary of the total booked time of all cars, organized by car. No parameters required.
    """
    results = Database.select_record_parameterized(
        " CarID, CONVERT(SUM(TIMESTAMPDIFF(MINUTE, RentTime, ReturnTime)), SIGNED) AS Total", 
        " Bookings ", 
        " WHERE Status = 'Booked' GROUP BY CarID",
        ()
    ) 
    return {"results": results}

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
    return results[0]

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
        " OR CustomerID = %(customer_id)s ",
         {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id")
        }
    )
    return {"bookings" : results}

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
        " AND RentTime >= %(start)s AND ReturnTime <= %(end)s ",
         {
            "car_id": request.args.get("car_id"),
            "customer_id": request.args.get("customer_id"), 
            "start": request.args.get("start"), 
            "end": request.args.get("end")
        }
    )
    return {"bookings" : results}

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
