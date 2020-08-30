"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

import requests
from model.server import Server
from model.code import Code
from model.account import Account

server = None

def listen_to_client():
    while True:
        # Constantly display message received from server until the end of connection (receive good bye message)
        message = server.receive_message()
        if message == "end":
            # Close socket after connection is closed
            server.close_connection()
            break
        else:
            handle_request(message)
    
def handle_request(message):
    try:
        message = Code.parse_json(message.replace("\'", "\""))
        if message["message_type"] == "credential":
            validate_crendential(message)
        elif message["message_type"] == "car_status":
            update_car_status(message)
    except:
        pass

# Validate credential
def validate_crendential(message):
    if Account.verify_password(message["username"], message["password"], message["user_type"]):
        server.send_message("valid")
    else:
        server.send_message("invalid")

# Validate credential
def update_car_status(message):
    resp = requests.get(
		"http://127.0.0.1:8080/cars/update?" +
		"status=" + message["car_status"] +
		"&id=" + message["car_id"]
	)
    server.send_message(resp.text)

if __name__ == "__main__":
    server = Server()
    listen_to_client()