from flask import Blueprint, request, jsonify
import json
from model.database import Database
from model.util import Util

customer_api = Blueprint("customer_api", __name__)

@customer_api.route("/create", methods=['GET', 'POST'])
def create():
    try:
        Database.insert_record_parameterized(
            "Customers(Username, Password, FirstName, LastName, Email, Phone)",
            "(%s, %s, %s, %s, %s, %s)",
            (
                request.args.get("username"),
                request.args.get("password"),
                request.args.get("first_name"),
                request.args.get("last_name"),
                request.args.get("email"),
                request.args.get("phone"),
            )
        )
        return "Success"
    except:
        return "Fail"

@customer_api.route("read")
def read():
    results = Database.select_record_parameterized(
        "*", 
        "Customers", 
        " WHERE Username LIKE CASE WHEN %(username)s = '' OR %(username)s IS NULL " +
        " THEN Username ELSE %(username)s END " +
        " AND FirstName LIKE CASE WHEN %(first_name)s = '' OR %(first_name)s IS NULL " +
        " THEN FirstName ELSE %(first_name)s END " +
        " AND LastName LIKE CASE WHEN %(last_name)s = '' OR %(last_name)s IS NULL " + 
        " THEN LastName ELSE %(last_name)s END " +
        " AND Email LIKE CASE WHEN %(email)s = '' OR %(email)s IS NULL " + 
        " THEN Email ELSE %(email)s END " +
        " AND Phone LIKE CASE WHEN %(phone)s = '' OR %(phone)s IS NULL " + 
        " THEN Phone ELSE %(phone)s END ",
        {
            "username": request.args.get("username"), 
            "first_name": request.args.get("first_name"),
            "last_name": request.args.get("last_name"), 
            "email": request.args.get("email"),
            "phone": request.args.get("phone")
        }
    ) 
    return {"results:": Util.paginatedDisplay(results, request.args.get("page"))}

@customer_api.route("/update", methods=['GET', 'PUT'])
def update():
    try:
        Database.update_record_parameterized(
            "Customers",
            " Username = CASE WHEN %(username)s = '' OR %(username)s IS NULL " +
            " THEN Username ELSE %(username)s END, " +
            " Password = CASE WHEN %(password)s = '' OR %(password)s IS NULL " +
            " THEN Password ELSE %(password)s END, " +
            " FirstName = CASE WHEN %(first_name)s = '' OR %(first_name)s IS NULL " + 
            " THEN FirstName ELSE %(first_name)s END, " +
            " LastName = CASE WHEN %(last_name)s = '' OR %(last_name)s IS NULL " + 
            " THEN LastName ELSE %(last_name)s END, " +
            " Email = CASE WHEN %(email)s = '' OR %(email)s IS NULL " + 
            " THEN Email ELSE %(email)s END, " +
            " Phone = CASE WHEN %(phone)s = '' OR %(phone)s IS NULL " + 
            " THEN Phone ELSE %(phone)s END ",
            " WHERE ID = %(customer_id)s", 
            {
                "customer_id": request.args.get("id"),
                "username": request.args.get("username"), 
                "password": request.args.get("password"), 
                "first_name": request.args.get("first_name"),
                "last_name": request.args.get("last_name"), 
                "email": request.args.get("email"),
                "phone": request.args.get("phone")
            }
        )
        return "Success"
    except:
        return "Fail"
    
@customer_api.route("/delete", methods=['GET', 'DELETE'])
def delete():
    try:
        Database.delete_record_parameterized(
            "Customers",
            " WHERE ID = %s"
            , request.args.get("id"),
        )
        return "Success"
    except:
        return "Fail"

@customer_api.route("/check/email/and/phone/combination")
def check_email_phone_combination():
    result = Database.select_record_parameterized(
        "COUNT(*) AS SUM ", 
        " Customers ", 
        " WHERE Email = %s AND Phone = %s", 
        (request.args.get("email"), request.args.get("phone"))
    )
    return result[0]

@customer_api.route("/get/encrypted/password")
def get_encrypted_password():
    results = Database.select_record_parameterized(
        " Password ", 
        " Customers ", 
        " WHERE Username = %s ", 
        (request.args.get("username"),)
    ) 
    return {"passwords": results}

@customer_api.route("/check/existed/username")
def check_username():
    result = Database.select_record_parameterized(
        " COUNT(*) AS SUM ", 
        " Customers ", 
        " WHERE Username = %s", 
        (request.args.get("username"),)
    )
    return result[0]
