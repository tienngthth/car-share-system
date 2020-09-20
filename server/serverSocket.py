"""
serverSocket.py
====================================
This contains the functions that listen for client requests. It also handles user validation, and otherwise routes different request types, e.g. check_backlog, to the appropriate function. We use UTF-8 encoding for all requests.
"""

# !/usr/bin/env python3


import requests, json
from server import Server
from passlib import hash

def listen_to_client():
    """
    Constantly handle request from client until receiving end signal
    """
    while True:
        message = server.receive_message()
        if message == "end":
            server.close_connection()
        elif message != "":
            handle_request(message)
    
def handle_request(message):
    """
    Route a request to the correct handler. Parameters:

    message: must be credential, check_backlog, update_car_status, close_backlog, or get_car_id. Otherwise will return Invalid.
    """
    try:
        message = json.loads(message.replace("\'", "\""))
        message_type = message["message_type"]
        if message_type == "credential":
            validate_crendential(message)
        elif message_type == "check_backlog":
            check_for_car_maintainance(message)
        elif message_type == "update_car_status" or message_type == "close_backlog":
            update_car_status(message)
        elif message_type == "get_car_id":
            get_car_id_by_ap_addr(message)
    except:
        server.send_message("invalid")

# Validate credential
def validate_crendential(message):
    """
    Check if a username+password pair is a valid user, passing the password on to a dedicated password validation function. If valid, returns the user's bookings for a particular car. Parameters:

    message: must contain a username and password, along with the car ID and customer_id. If the authentication fails, returns Invalid.
    """
    user = verify_password(message["username"], message["password"])
    if user != "invalid":
        booking = requests.get(
            "http://127.0.0.1:8080/bookings/read?car_id=" + message["car_id"] + 
            "customer_id" + message["customer_id"]
        ).json()["bookings"]
        if len(booking) != 0:
            server.send_message(user["Password"])
            return
    server.send_message("invalid")


def verify_password(username, input_password):
    """
    Verify the password of a user. Passwords are stored as SHA256 hashes of the password plaintext, so we hash the password before comparing to what's stored in the database. Parameters:

    username: A username must be specified
    input_password: The password must be specified.
    If there are any missing fields or the username+password pair is not recognized, returns Invalid
    """
    try:
        user = requests.get("http://127.0.0.1:8080/get/user/info?username="+username).json()
        if hash.sha256_crypt.verify(input_password, user["Password"]):
            return user
        return "invalid"
    except:
        return "invalid"

# Check for car maintainance
def check_for_car_maintainance(message):
    """
    Get the engineer assigned to repair a particular car, and the MAC address assigned to them. Parameters:
    
    message: must contain the car_id. Returns Invalid otherwise, or if no engineer is assigned to that car, or if the engineer assigned does not have a MAC address recorded.
    """
    engineer_id = requests.get("http://127.0.0.1:8080/backlogs/get/engineer/id?car_id=" + str(message["car_id"])).json()["AssignedEngineerID"]
    if engineer_id != "No engineer found":
        engineer_mac_address = requests.get("http://127.0.0.1:8080/staffs/get/engineer/mac/address?id=" + str(engineer_id)).json()["EngineerMacAddress"]
        if engineer_mac_address != "No mac address found":
            server.send_message(engineer_mac_address)
            return
    server.send_message("invalid")

# Update car status
def update_car_status(message):
    """
    Update a car's status, for example to mark it as available, or requiring repairs. Parameters:

    message: if the message type is close_backlog, it closes the backlog entry
             Otherwise, it will look for car_status and car_id, and apply that status to the given car
    """
    requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + message["car_status"] +
		"&id=" + str(message["car_id"])
	)
    # Close backlog
    if message["message_type"] == "close_backlog":
        requests.put(
            "http://127.0.0.1:8080/backlogs/close?" + 
            "signed_engineer_id=" + str(message["engineer_id"]) + "&car_id=" +  str(message["car_id"])
        )
    
# Get car id by ap mac address
def get_car_id_by_ap_addr(message):
    """
    Get a car's ID using the MAC address of the Agent Pi. Parameters:

    message: Searches for a car id if the message contains ap_addr, which must be a MAC address. If none are found, returns Invalid.
    """
    car_id = requests.get("http://127.0.0.1:8080/cars/get/id?mac_address=" + message["ap_addr"]).json()["ID"]
    if car_id == "No car found":
        server.send_message("invalid")
    else:
        server.send_message(str(car_id))

if __name__ == "__main__":
    global server
    server = Server()
    listen_to_client()
