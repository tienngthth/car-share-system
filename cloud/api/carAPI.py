"""
carAPI.py defines all the functions regarding CRUD on cars, as well as a car's booking history
"""

from flask import Blueprint, request
from database import Database

car_api = Blueprint("car_api", __name__)

@car_api.route("/create", methods=['GET', 'POST'])
def create():
    """
    This creates a new car. Parameters:
    
    mac_address: The MAC address of the car's agent Pi
    brand: The brand of the car e.g. Honda
    type: The make of the car, e.g. Civic
    location_id: The location of the car
    status: Whether the car requires repairs, is booked, or available
    color: The color of the car. We use a list of colors in the UI but Other is an option.
    seat: How many seats there are in the car
    cost: The hourly cost of renting the car
    
    Returns Done or an error
    
    """
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

@car_api.route("/update", methods=['GET', 'PUT'])
def update():
    """
    Updates a car. Functions the same as create()
    """
    try:
        Database.update_record_parameterized(
            " Cars ",
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
    """
    Deletes a car. Parameters:
    
    car_id: The car to delete
    
    Returns Success if a record was deleted, Fail otherwise
    """
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
    """
    This searches for a cars mathing a set of criteria. Parameters:
    
    mac_address: The MAC address of the car's agent Pi
    brand: The brand of the car e.g. Honda
    type: The make of the car, e.g. Civic
    location_id: The location of the car
    status: Whether the car requires repairs, is booked, or available
    color: The color of the car. We use a list of colors in the UI but Other is an option.
    seat: How many seats there are in the car
    cost: The hourly cost of renting the car
    
    Returns a dictionary containing cars that match the search criteria
    
    """
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
        " AND Type LIKE CASE WHEN %(car_type)s = '' OR %(car_type)s IS NULL " +
        " THEN Type ELSE %(car_type)s END " +
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
            "car_type": request.args.get("car_type"), 
            "status": request.args.get("status"), 
            "color": request.args.get("color"), 
            "seat": request.args.get("seat"), 
            "cost": request.args.get("cost")
        }
    ) 
    return {"cars": results}

@car_api.route("/status/available")
def get_available_car():
    """
    Gets only cars available for booking during a certian time period. Parameters are the same as read() except:
    
    start: The start time a customer wants to book for
    end: The time a customer wants to return the car
    
    Returns a dictionary of cars that match the search criteria.
    """
    results = Database.select_record_parameterized(
        " Cars.ID, Cars.Brand, Cars.Type, Cars.Color, Cars.MacAddress, " +
        " Cars.Seat, Locations.Address, Cars.Cost, Cars.Status",
        " Cars INNER JOIN Locations ON Cars.LocationID = Locations.ID ", 
        " WHERE MacAddress LIKE CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " +
        " THEN MacAddress ELSE %(mac_address)s END " +
        " AND Brand LIKE CASE WHEN %(brand)s = '' OR %(brand)s IS NULL " +
        " THEN Brand ELSE %(brand)s END " +
        " AND Type LIKE CASE WHEN %(car_type)s = '' OR %(car_type)s IS NULL " +
        " THEN Type ELSE %(car_type)s END " +
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
            "car_type": request.args.get("car_type"), 
            "color": request.args.get("color"), 
            "seat": request.args.get("seat"), 
            "cost": request.args.get("cost"),
            "start": request.args.get("start"),
            "end": request.args.get("end")
        }
    ) 
    return {"cars": results}

@car_api.route("get/id")
def get_car_id_by_mac_address():
    """
    Gets a car ID given the MAC address of its installed agent Pi. Parameters:
    
    mac_address: The mac address of the agent Pi
    
    Returns No car found if no results were found. Otherwise, returns the id of a car.
    """
    results = Database.select_record_parameterized(
        " ID ",
        " Cars ",
        " WHERE MacAddress = %s AND MacAddress NOT LIKE ''",
        (request.args.get("mac_address"),)
    )
    if len(results) == 0:
        return "No car found"
    else:
        return results[0]

@car_api.route("history")
def get_car_history():
    """
    Returns the booking history of a car. Parameters:
    
    id: the id of the car in question
    
    Returns the booking history of the car as a dictionary
    """
    results = Database.select_record_parameterized(
        " Bookings.ID, Bookings.CarID, Bookings.CustomerID, Bookings.RentTime, " +
        " Bookings.ReturnTime, Bookings.TotalCost, Bookings.Status ", 
        " Cars LEFT JOIN Bookings ON Cars.ID = Bookings.CarID ",
        " WHERE Cars.ID = %s",
        (request.args.get("id"),)
    )
    return {"history": results}
