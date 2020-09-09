from flask import Blueprint, request
from model.database import Database
# from model.util import Util

customer_api = Blueprint("customer_api", __name__)

@customer_api.route("/get/encrypted/password/by/username")
def get_encrypted_password_by_username():
    results = Database.select_record_parameterized(
        "Password", 
        "Customers", 
        " WHERE Username = %s", 
        request.args.get("username")
    ) 
    if len(results) == 0:
        return "No password found"
    else: 
        return results[0][0]

@customer_api.route("/get/number/of/existed/username")
def get_number_of_existed_username():
    result = Database.select_record_parameterized(
        "COUNT(*) ", 
        " Customers ", 
        " WHERE Username = %s", 
        request.args.get("username")
    )
    return str(result[0][0])

@customer_api.route("/get/number/of/existed/email/and/phone/combination")
def get_number_of_existed_email_phone_combination():
    result = Database.select_record_parameterized(
        "COUNT(*) ", 
        " Customers ", 
        " WHERE Email = %s AND Phone = %s", 
        (request.args.get("email"), request.args.get("phone"))
    )
    return str(result[0][0])

@customer_api.route("get/customers/by/filter")
def get_customer_by_filter():
    results = Database.select_record_parameterized(
        "*", 
        "Customers", 
        " WHERE Username LIKE %s" +
        " AND FirstName LIKE %s " +
        " AND LastName LIKE %s"
        " AND Email LIKE %s" +
        " AND Phone LIKE %s",
        (
            "%{}%".format(request.args.get("username")), 
            "%{}%".format(request.args.get("first_name")), 
            "%{}%".format(request.args.get("last_name")), 
            "%{}%".format(request.args.get("email")), 
            "%{}%".format(request.args.get("phone"))
        )
    ) 
    if len(results) == 0:
        return "No customer found"
    else: 
        # return str(Util.paginatedDisplay(results, int(request.args.get("page"))))
        pass

@customer_api.route("get/username/by/id")
def get_customer_username_by_id():
    results = Database.select_record_parameterized(
        "Username", 
        "Customers", 
        " WHERE ID = %s",
        request.args.get("id")
    )
    if len(results) == 0:
        return "No customer found"
    else:
        return results[0][0]

@customer_api.route("/create", methods=['GET', 'POST'])
def create_customer():
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
    return "Done"

@customer_api.route("/delete", methods=['GET', 'DELETE'])
def delete_customer():
    Database.delete_record_parameterized(
        "Customers",
        " WHERE ID = %s"
        , request.args.get("id"),
    )
    return "Done"

@customer_api.route("/update", methods=['GET', 'PUT'])
def update_customer():
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
    return "Done"