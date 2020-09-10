"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

import requests
from model.server import Server
from model.code import Code
from model.account import Account

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
            server.send_message(Account.hash_salt_password(message["password"]))
        elif message_type == "check_backlog":
            # check_for_car_maintainance()
            # server.send_message("34:E1:2D:A6:24:75") # lap cuong
            assigned_engineer_info = {"mac_address":"44:03:2C:9F:9A:BF", "engineer_id" : "3"}
            server.send_message(str(assigned_engineer_info))
            # server.send_message("invalid") # car no need to maintain
        elif message_type == "update_car_status" or message_type == "close_backlog":
            # update_car_status(message)
            pass
        elif message_type == "get_car_id":
            server.send_message("1") 
            # pass
    except:
        server.send_message("invalid")

def get_car_id_by_ap_addr(message):
    return requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + message["ap_addr"]
	).text

def check_for_car_maintainance():
    engineer_id = get_assigned_engineer_id_by_car_id(message["car_id"])
    if engineer_id != "No engineer found":
        engineer_mac_address = get_assigned_engineer_mac_addr_by_id(engineer_id)
        if mac_address != "No mac address found":
            server.send_message(mac_address)
    server.send_message("invalid")

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
    if Account.verify_credential(message["password"], encrypted_password):
        server.send_message(encrypted_password)
    else:
        server.send_message("invalid")

def get_encrypted_password_by_username(message):
    return requests.get(
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
    if message["message_type"] == "close_backlog":
        update_backlog(message["car_id"])
    
# Close ticket and save signed engineer id
def update_backlog(car_id):
	requests.put(
		"http://127.0.0.1:8080/backlogs/update/signed/engineer/id/and/status/by/car/id?" +
		"signed_engineer_id=" + message["engineer_id"] +
		"&car_id=" + car_id
	)

if __name__ == "__main__":
    global server
    server = Server()
    listen_to_client()
