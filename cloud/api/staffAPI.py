"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Blueprint, request
from database import Database
from flask.json import jsonify

staff_api = Blueprint("staff_api", __name__)

@staff_api.route("read")
def read():
    results = Database.select_record_parameterized(
        " * ", 
        " Staffs ", 
        " WHERE ID LIKE CASE WHEN %(id)s = '' OR %(id)s IS NULL " +
        " THEN ID ELSE %(id)s END " +
        " AND Username LIKE CASE WHEN %(username)s = '' OR %(username)s IS NULL " +
        " THEN Username ELSE %(username)s END " +
        " AND FirstName LIKE CASE WHEN %(first_name)s = '' OR %(first_name)s IS NULL " +
        " THEN FirstName ELSE %(first_name)s END " +
        " AND LastName LIKE CASE WHEN %(last_name)s = '' OR %(last_name)s IS NULL " + 
        " THEN LastName ELSE %(last_name)s END " +
        " AND Email LIKE CASE WHEN %(email)s = '' OR %(email)s IS NULL " + 
        " THEN Email ELSE %(email)s END " +
        " AND Phone LIKE CASE WHEN %(phone)s = '' OR %(phone)s IS NULL " + 
        " THEN Phone ELSE %(phone)s END " +
        " AND UserType LIKE CASE WHEN %(user_type)s = '' OR %(user_type)s IS NULL " +
        " THEN UserType ELSE %(user_type)s END ",
        {
            "id": request.args.get("id"), 
            "username": request.args.get("username"), 
            "first_name": request.args.get("first_name"),
            "last_name": request.args.get("last_name"), 
            "email": request.args.get("email"),
            "phone": request.args.get("phone"),
            "user_type": request.args.get("user_type")
        }
    )
    return jsonify(results)

@staff_api.route("/check/existed/username")
def check_username():
    result = Database.select_record_parameterized(
        " COUNT(*) AS SUM ", 
        " Staffs ", 
        " WHERE Username = %s", 
        (request.args.get("username"),)
    )
    return str(result[0]["SUM"])

@staff_api.route("get/engineer/mac/address")
def get_engineer_mac_address():
    results = Database.select_record_parameterized(
        " EngineerMacAddress ", 
        " Staffs ", 
        " WHERE ID = %s", 
        (request.args.get("id"), )
    ) 
    if len(results) == 0:
        return "No mac address found"
    else:
        return str(results[0]["EngineerMacAddress"])

@staff_api.route("/delete", methods=['GET', 'DELETE'])
def delete():
    try:
        Database.delete_record_parameterized(
            " Staffs ",
            " WHERE ID = %s"
            , (request.args.get("id"),)
        )
        return "Success"
    except:
        return "Fail"