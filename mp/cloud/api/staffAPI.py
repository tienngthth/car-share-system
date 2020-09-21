#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
staffAPI handles user queries that are only for staff members, e.g. admin users.
"""

from flask import Blueprint, request
from database import Database

staff_api = Blueprint("staff_api", __name__)

@staff_api.route("read")
def read():
    """
    Searches for all users that match a set of criteria. Parameters:

    id: The user's id
    username: The user's username
    first_name: The user's first name
    last_name: The user's last name
    email: The user's email address. Validated elsewhere by regex.
    phone: The user's phone number
    user_type: The type of user -- engineer, admin, manager, customer.
    
    Returns a dictionary containing all matches.
    
    """
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
    return {"staffs": results}

@staff_api.route("/check/existed/username")
def check_username():
    """
    Checks if a username exists. Parameters:
    
    username: the username of the user
    
    Returns 0 if the username does not exist, otherwise returns a count of the number of users with that name. Should never exceed 1.
    """
    result = Database.select_record_parameterized(
        " COUNT(*) AS SUM ", 
        " Staffs ", 
        " WHERE Username = %s", 
        (request.args.get("username"),)
    )
    return str(result[0]["SUM"])

@staff_api.route("get/engineer/mac/address")
def get_engineer_mac_address():
    """
    Get the MAC address of an engineer given their ID. Parameters:
    
    id: The user ID of the engineer
    
    Returns no mac address found if the length of results is zero. Otherwise, returns the user ID of the engineer.
    """
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

@staff_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            " Staffs ",
            " Username = CASE WHEN %(username)s = '' OR %(username)s IS NULL " +
            " THEN Username ELSE %(username)s END, " +
            " FirstName = CASE WHEN %(first_name)s = '' OR %(first_name)s IS NULL " + 
            " THEN FirstName ELSE %(first_name)s END, " +
            " LastName = CASE WHEN %(last_name)s = '' OR %(last_name)s IS NULL " + 
            " THEN LastName ELSE %(last_name)s END, " +
            " Email = CASE WHEN %(email)s = '' OR %(email)s IS NULL " + 
            " THEN Email ELSE %(email)s END, " +
            " Phone = CASE WHEN %(phone)s = '' OR %(phone)s IS NULL " + 
            " THEN Phone ELSE %(phone)s END, " +
            " EngineerMacAddress = CASE WHEN %(mac_address)s = '' OR %(mac_address)s IS NULL " + 
            " THEN EngineerMacAddress ELSE %(mac_address)s END " ,
            " WHERE ID = %(id)s", 
            {
                "id": request.args.get("id"),
                "username": request.args.get("username"), 
                "password": request.args.get("password"), 
                "first_name": request.args.get("first_name"),
                "last_name": request.args.get("last_name"), 
                "email": request.args.get("email"),
                "phone": request.args.get("phone"),
                "mac_address": request.args.get("mac_address")
            }
        )
        return "Success"
    except:
        return "Fail"
