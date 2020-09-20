"""
locationAPI.py contains only a function to return details on a given location.
"""
from flask import Blueprint, request
from database import Database

location_api = Blueprint("location_api", __name__)

@location_api.route("get")
def get_location():
    """
    This returns details (e.g. latitude, longitude) of a defined location. Parameters:
    
    id: The id of the location in question
    
    Returns a dictionary with the location details.
    """
    results = Database.select_record_parameterized(
        " * ", 
        " Locations ",
        " WHERE Locations.ID = %s",
        (request.args.get("id"),)
    )
    return {"location": results}
