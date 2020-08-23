#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.client import Client
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
        if message["type"] == credential:
            validate_crendential()
        elif message["type"] == car_status:
            update_car_status()
    except:
        pass


# Validate credential
def validate_crendential():
    if Account.verify_password(message["username"], message["password"]):
        server.send_message("valid")
    else:
        server.send_message("invalid")

# Validate credential
def update_car_status():
    #Up car availability - user first login/return
    pass

# Function to call when Pi is a client
def run_client():
    client = Client()
    # do something
    client.close_socket()

if __name__ == "__main__":
    run_server()