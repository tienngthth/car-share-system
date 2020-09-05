#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bluetooth
from time import sleep
from model import car

# Search for engineer device with matched mac address
def start_searching(device_mac_address = ""):
    # Wait until bluetooth is on and stable (loop throught the unstable period)
    while True:         
        try:
            sleep(5)
            # Get all nearby devices mac address
            nearby_devices_mac_address = bluetooth.discover_devices()
            # Loop through all nearby devices
            for mac_address in nearby_devices_mac_address:
                if mac_address == device_mac_address:
                    engineer_found = True
            if engineer_found:
                car.lock_status = "unlock"
            else:
                car.lock_status = "lock"
        except:
            start_searching()
