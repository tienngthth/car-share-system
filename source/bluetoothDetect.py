#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bluetooth
from time import sleep

# Search for device containing keyword
def start_searching(server_mac_address = "", server_name = "CuongvTien"):
    while True:
        # Wait until bluetooth is on and stable
        try:
            sleep(5)
            # Get all nearby devices mac address
            nearby_devices_mac_address = bluetooth.discover_devices()
            # Loop through all nearby devices
            for mac_address in nearby_devices_mac_address:
                if mac_address == server_mac_address:
                    engineer_found = True
            if engineer_found:
                pass
                #Unlock car
            else:
                #Lock car
                pass
        except:
            start_searching()

if __name__ == "__main__":
    start_searching()