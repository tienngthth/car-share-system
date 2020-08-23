#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.client import Client
from model.server import Server

server = Server()

# Function to call when Pi is a server
def run_server():
    #Receive message from client -> validate/update car status
    pass

# Validate credential
def validate_crendential():
    #Validate credential -> send result to client
    pass

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