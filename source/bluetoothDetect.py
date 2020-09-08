#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bluetooth
from time import sleep

# Search for engineer device with matched mac address
def start_searching(car_lock = True, device_mac_address = ""):
    # Wait until bluetooth is on and stable (loop throught the unstable period)
    while True:         
        if find_eng(device_mac_address):
            close_ticket_menu()

def find_eng(device_mac_address = ""):
    try:
        sleep(5)
        # Get all nearby devices mac address
        nearby_devices_mac_address = bluetooth.discover_devices()
        # Loop through all nearby devices
        for mac_address in nearby_devices_mac_address:
            if mac_address == device_mac_address:
                engineer_found = True
        if engineer_found:
            return True
        else:
            return False
    except:
        find_eng(device_mac_address)


def close_ticket_menu():
    print("Car Unlocked! Application menu")
    print("Lock car: Press key \"L\"")
    print("Close backlog (scan QR code): Press key \"C\"")
    while find_eng():  
        option = Util.get_input("Option: ").lower().strip()
        if option == "q":  
            break
        elif option == "l":
            break
    print('Car locked!\n')

if __name__ == "__main__":
    start_searching()