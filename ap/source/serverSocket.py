"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from server import Server
from passlib import hash
from model.code import Code
import requests, json

def listen_to_client():
    # Constantly handle request from client until receiving end signal
    while True:
        message = server.receive_message()
        if message == "end":
            server.close_connection()
        elif message != "":
            handle_request(message)
    
def handle_request(message):
    try:
        message = Code.parse_json(message.replace("\'", "\""))
        message_type = message["message_type"]
        if message_type == "credential":
            # validate_crendential(message)
            server.send_message(str({"password": hash.sha256_crypt(message["Password"]), "booking_id": 1}))
        elif message_type == "check_backlog":
            # check_for_car_maintainance(message)
            server.send_message(str({"mac_address": "DC:F7:56:2D:C1:97", "engineer_id": 1}))
        elif message_type == "update_car_status" or message_type == "close_backlog":
            # update_car_status(message)
            pass
        elif message_type == "update_car_status":
            # update_car_status(message)
            pass
        elif message_type == "get_car_id":
            # get_car_id_by_ap_addr(message)
            server.send_message("1")
        elif message_type == "done_booking":
            # done_booking(message)
            pass
    except:
        server.send_message("invalid")

# Validate credential
def validate_crendential(message):
    user = verify_password(message["username"], message["password"])
    if user != "invalid":
        booking = requests.get(
            "http://127.0.0.1:8080/bookings/read?car_id=" + message["car_id"] + 
            "customer_id" + message["customer_id"]
        ).json()
        if len(booking) != 0:
            change_car_status("In use", message["car_id"])
            update_booking_status("In use", booking["ID"])
            server.send_message(str({"password": user["Password"], "booking_id": booking["ID"]}))
            return
    server.send_message("invalid")

def verify_password(username, input_password):
    try:
        user = requests.get("http://127.0.0.1:8080/get/user/info?username="+username).json()
        if hash.sha256_crypt.verify(input_password, user["Password"]):
            return user
        return "invalid"
    except:
        return "invalid"

# Update car status
def done_booking(message):
    update_booking_status("Done", message["booking_id"])

# Update car status
def update_booking_status(status, booking_id):
    requests.put("http://127.0.0.1:8080/bookings/update?" + "status=" + status + "&id=" + booking_id)

# Check for car maintainance
def check_for_car_maintainance(message):
    engineer_id = requests.get("http://127.0.0.1:8080/backlogs/get/engineer/id?car_id=" + message["car_id"]).json()
    if engineer_id != "No engineer found":
        engineer_mac_address = requests.get("http://127.0.0.1:8080/staffs/get/engineer/mac/address?id=" + str(engineer_id)).text
        if engineer_mac_address != "No mac address found":
            server.send_message(engineer_mac_address)
            return
    server.send_message("invalid")

# Update car status
def update_car_status(message):
    change_car_status(message["car_status"], message["car_id"])
    # Close backlog
    if message["message_type"] == "close_backlog":
        close_backlog(message["engineer_id"], message["car_id"])
        
def change_car_status(status, car_id):
    requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + status +
		"&id=" + car_id
	)

def close_backlog(engineer_id, car_id):
    requests.put(
        "http://127.0.0.1:8080/backlogs/close?" + 
        "signed_engineer_id=" + engineer_id + "&car_id=" +  car_id
    )
    
# Get car id by ap mac address
def get_car_id_by_ap_addr(message):
    car_id = requests.get("http://127.0.0.1:8080/cars/get/id?mac_address=" + message["ap_addr"]).text
    if car_id == "No car found":
        server.send_message("invalid")
    else:
        server.send_message(str(car_id))

if __name__ == "__main__":
    global server
    server = Server()
    listen_to_client()