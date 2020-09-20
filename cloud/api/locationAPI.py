"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Blueprint, request
from database import Database
from flask.json import jsonify

location_api = Blueprint("location_api", __name__)

@location_api.route("get")
def get_location():
    results = Database.select_record_parameterized(
        " * ", 
        " Locations ",
        " WHERE Locations.ID = %s",
        (request.args.get("id"),)
    )
    return jsonify(results)