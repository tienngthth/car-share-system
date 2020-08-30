#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.server import Server
from model.code import Code
from model.account import Account

server = Server()
credential = 1
car_status = 2
message = {}

# Function to call when Pi is a server
def run_server():
    #Receive message from client -> validate/update car status
    try:
        message = Code.parse_json(server.receive_message())
        if message["message_type"] == "credential":
            validate_crendential()
        elif message["message_type"] == "car_status":
            update_car_status()
    except:
        pass

# Validate credential
def validate_crendential():
    if Account.verify_password(message["password"], message["username"], message["user_type"]):
        server.send_message("valid")
    else:
        server.send_message("invalid")

# Validate credential
def update_car_status():
    resp = requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + message["car_status"] +
		"&id=" + message["car_id"]
	)
    print(resp.text)

if __name__ == "__main__":
    run_server()