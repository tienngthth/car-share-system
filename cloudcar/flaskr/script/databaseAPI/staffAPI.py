from flask import Blueprint, request
from model.database import Database


staff_api = Blueprint("staff_api", __name__)

@staff_api.route("/get/encrypted/password")
def get_encrypted_password():
    results = Database.select_record_parameterized(
        " Password ", 
        " Staffs ", 
        " WHERE Username = %s ", 
        (request.args.get("username"), )
    ) 
    return {"passwords": results}

@staff_api.route("get/admin")
def get_admin():
    results = Database.select_record_parameterized(
        " * ", 
        " Staffs ", 
        " WHERE UserType = 'Admin' AND Username = %s OR ID = %s", 
        (request.args.get("username"), request.args.get("id"))
    ) 
    return {"admin": results}

@staff_api.route("get/manager")
def get_manager():
    results = Database.select_record_parameterized(
        " * ", 
        " Staffs ", 
        " WHERE UserType = 'Manager' AND Username = %s OR ID = %s", 
        (request.args.get("username"), request.args.get("id"))
    ) 
    return {"manager": results}

@staff_api.route("get/engineer")
def get_engineer():
    results = Database.select_record_parameterized(
        " * ", 
        " Staffs ", 
        " WHERE UserType = 'Engineer' AND Username = %s OR ID = %s", 
        (request.args.get("username"), request.args.get("id"))
    ) 
    return {"engineer": results}