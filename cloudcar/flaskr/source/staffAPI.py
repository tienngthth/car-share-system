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
