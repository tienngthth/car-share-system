from flask import Blueprint, request
from model.database import Database


staff_api = Blueprint("staff_api", __name__)

@staff_api.route("/get/encrypted/password/by/username")
def get_encrypted_password_by_username():
    results = Database.select_record_parameterized(
        "Password", 
        "Staffs", 
        " WHERE Username = %s", 
        request.args.get("username")
    ) 
    if len(results) == 0:
        return "No password found"
    else: 
        return results[0][0]

@staff_api.route("/get/engineer/mac/address/by/id")
def get_engineer_mac_address_by_id():
    results = Database.select_record_parameterized(
        " MacAddress ", 
        " Staffs ", 
        " WHERE ID = %s ",
        (request.args.get("id"), )
    ) 
    if len(results) == 0:
        return "No mac address found"
    else: 
        return str(results[0][0])
