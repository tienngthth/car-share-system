from flask import Blueprint
from model.database import Database

customer_api = Blueprint("customer_api", __name__)

@customer_api.route("/customers/get/encrypted/password/<username>")
def get_encrypted_password(username):
    results = Database.select_record_parameterized(
        "Password", 
        "Customers", 
        " WHERE username = %s", 
        username
    ) 
    if len(results) == 0:
        return "No password found"
    else: 
        return results[0][0]

