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

