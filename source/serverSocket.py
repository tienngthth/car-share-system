"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

import requests
from model.server import Server
from model.code import Code
from model.account import Account
from model.car import car

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
        if message["message_type"] == "credential":
            # validate_crendential(message)
            server.send_message(Account.hash_salt_password(message["password"]))
        elif message["message_type"] == "backlog":
            # check_for_car_maintainance()
            server.send_message("34:E1:2D:A6:24:75") # lap cuong
        elif message["message_type"] == "car_status":
            # update_car_status(message)
            pass
    except:
        server.send_message("invalid")
 
def check_for_car_maintainance():
    car_id = get_car_id_by_ap_addr()
    engineer_id = get_assigned_engineer_id_by_car_id(car_id)
    if engineer_id != "No engineer found":
        engineer_mac_address = get_assigned_engineer_mac_addr_by_id(engineer_id)
        if mac_address != "No mac address found":
            server.send_message(mac_address)
    server.send_message("invalid")

def get_car_id_by_ap_addr():
    return requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + car.ap_addr
	).text

def get_assigned_engineer_id_by_car_id(car_id):
    return requests.get(
        "http://127.0.0.1:8080/backlogs/get/engineer/id/by/car/id?" +
		"car_id=" + car_id
	).text

def get_assigned_engineer_mac_addr_by_id(engineer_id):
    return requests.get(
        "http://127.0.0.1:8080/staffs/get/engineer/mac/address/by/id?" +
        "id=" + engineer_id
    ).text

# Validate credential
def validate_crendential(message):
    encrypted_password = get_encrypted_password_by_username(message)
    if Account.verify_credential(message["password"], encrypted_password)):
        server.send_message(encrypted_password)
    else:
        server.send_message("invalid")

def get_encrypted_password_by_username(message):
    return encrypted_password = requests.get(
        "http://127.0.0.1:8080/" +
        message["user_type"] +
        "/get/encrypted/password/by/username?username=" +
        message["username"]
    ).text

def update_car_status(message):
    resp = requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + message["car_status"] +
		"&id=" + message["car_id"]
	)
    server.send_message(resp.text)

if __name__ == "__main__":
    global server
    server = Server()
    listen_to_client()
