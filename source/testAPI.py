#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

data_send = None

# Function to call GET API to get the latest context from the database
def test_get_api():
    resp = requests.get('http://127.0.0.1:8080/get/newest/context')
    if str(resp.content).find("Fail") != -1:
        print(resp.content)
    else:
        print(resp.json())

# Function to call PUT API to upload new context from the database
def upload_api():
    resp = requests.post(
        'http://127.0.0.1:8080/upload/context',
        data = json.dumps(data_send),
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )
    print(resp.content)
    # Call function to get the latest context and check if its uploaded as required, test GET API at the same time
    if str(resp.content).find("Successfully") != -1:
        test_get_api()

# Function to call PUT API to update the latest context from the database
def update_api():
    resp = requests.put(
        'http://127.0.0.1:8080/update/newest/context',
        data = json.dumps(data_send),
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )
    print(resp.content)
        
if __name__ == "__main__":
    try:
        test_upload_api()
        test_update_api()
    except:
        # Print error if can not connect to server
        print("Can not connect to server")