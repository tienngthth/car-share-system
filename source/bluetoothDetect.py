#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bluetooth
from time import sleep
from model.util import Util
from qrcodeScanner import start_scanning
from model.client import Client

def get_engineer_mac_address():
    global engineer_mac_address 
    client = Client()
    repair_car_message = {"message_type":"backlog"}
    engineer_mac_address = wait_for_response(client, repair_car_message)

def wait_for_response(client, message):
    client.send_message(str(message))
    while True:
        message = client.receive_message()
        if message != "":
            client.send_message("end")
            return message

# Search for engineer device with matched mac address
def start_searching():
    get_engineer_mac_address()
    if engineer_mac_address != "invalid"::
        print("\nSearching for engineer...")
        find_engineer()
        if engineer_found:
            close_ticket_menu()
        else:
            print("\nNo engineer found. Stop searching")
    else:
        print("No maintanance needed")

def find_engineer():
    global engineer_found
    # Wait until bluetooth is on and stable (loop throught the unstable period)
    for i in range(2):         
        try:
            sleep(2)
            # Get all nearby devices mac address
            nearby_devices_mac_address = bluetooth.discover_devices()
            # Loop through all nearby devices
            for mac_address in nearby_devices_mac_address:
                if mac_address == engineer_mac_address:
                    engineer_found = True
                    return
        except:
            find_engineer()
    engineer_found = False

def close_ticket_menu():
    print("\nCar Unlocked! Application menu")
    print("Lock car: Press key \"L\"")
    print("Close backlog (scan QR code): Press key \"C\"")
    while engineer_found:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "c":  
            start_scanning()
            break
        elif option == "l":
            break
        find_engineer()
    print("\nCar locked!")

if __name__ == "__main__":
    find_engineer()