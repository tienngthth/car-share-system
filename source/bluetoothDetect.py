#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bluetooth
from time import sleep

# Search for engineer device with matched mac address
def start_searching(device_mac_address = ""):
    print("\nSearching for engineer...")
    # Wait until bluetooth is on and stable (loop throught the unstable period)
    for i in range(1):         
        try:
            sleep(2)
            # Get all nearby devices mac address
            nearby_devices_mac_address = bluetooth.discover_devices()
            # Loop through all nearby devices
            for mac_address in nearby_devices_mac_address:
                if mac_address == device_mac_address:
                    close_ticket_menu()
                    return
            print("\nNo engineer found. Continue searching...")
        except:
            find_eng(device_mac_address)

    print("\nNo engineer found. Stop searching")


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
    print("\nCar locked!")

if __name__ == "__main__":
    start_searching()