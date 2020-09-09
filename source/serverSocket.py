"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

import requests
from model.server import Server
from model.code import Code
from model.account import Account
from model.car import car

server = None

def listen_to_client():
    while True:
        # Constantly display message received from server until the end of connection (receive good bye message)
        message = server.receive_message()
        if message == "end":
            # Close socket after connection is closed
            server.close_connection()
        elif message != "":
            handle_request(message)
    
def handle_request(message):
    try:
        message = Code.parse_json(message.replace("\'", "\""))
        if message["message_type"] == "credential":
            # validate_crendential(message)
            server.send_message(Account.hash_salt_password(message["password"]))
        elif message["message_type"] == "facial":
            # validate_facial(message)
            server.send_message(Account.hash_salt_password("hashedPassword"))
        elif message["message_type"] == "backlog":
            # validate_facial(message)
            server.send_message("34:E1:2D:A6:24:75")# lap cuong
        elif message["message_type"] == "car_status":
            # update_car_status(message)
            pass
    except:
        pass
 
def check_for_car_maintainance():
    car_id = requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + car.ap_addr
	).text
    engineer_id = requests.get(
        "http://127.0.0.1:8080/backlogs/get/engineer/id/by/car/id?" +
		"car_id=" + car_id
	).text
    if engineer_id != "No engineer found":
        engineer_mac_address = requests.get(
            "http://127.0.0.1:8080/staffs/get/engineer/mac/address/by/id?" +
            "id=" + engineer_id
	    ).text
        if mac_address != "No mac address found":
            return mac_address
    return "Invalid"    

def validate_facial(message):
    car_id = requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + car.ap_addr
	).text
    customer_id = requests.get(
        "http://127.0.0.1:8080/bookings/get/current/customer/id/by/car/id?" +
		"car_id=" + car_id
	).text
    username = requests.get(
		"http://127.0.0.1:8080/customers/get/username/by/id?" +
		"id=" + customer_id
	).text
    if message["username"] == username:
        return requests.get(
            "http://127.0.0.1:8080/customers/get/encrypted/password/by/username?" +
            "username=" + username
	    ).text
    else:
        return "invalid"

# Validate credential
def validate_crendential(message):
    if Account.verify_password(message["username"], message["password"], message["user_type"]):
        return requests.get(
            "http://127.0.0.1:8080/customers/get/encrypted/password/by/username?" +
            "username=" + message["username"]
	    ).text
    else:
        server.send_message("invalid")

# Validate credential
def update_car_status(message):
    resp = requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + message["car_status"] +
		"&id=" + message["car_id"]
	)
    server.send_message(resp.text)

if __name__ == "__main__":
    server = Server()
    listen_to_client()
