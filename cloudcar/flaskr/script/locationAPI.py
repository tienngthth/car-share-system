from flask import Blueprint, request
from model.database import Database
from model.util import Util

location_api = Blueprint("location_api", __name__)

@location_api.route("get")
def get_location():
    results = Database.select_record_parameterized(
        " * ", 
        " Locations ",
        " WHERE Locations.ID = %s",
        request.args.get("id")
    )
    return {"location": results}