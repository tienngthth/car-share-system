"""# !/usr/bin/env python3
# -*- coding: utf-8 -*-"""
import bluetooth
from time import sleep
from model import car

# Search for engineer device with matched mac address
def start_searching(device_mac_address = ""):
    engineer_found = False
    # Get all nearby devices mac address
    nearby_devices_mac_address = bluetooth.discover_devices()
    # Loop through all nearby devices
    for mac_address in nearby_devices_mac_address:
        if mac_address == device_mac_address:
            engineer_found = True
    return engineer_found

if __name__ == "__main__":
    start_searching()