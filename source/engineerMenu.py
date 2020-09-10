#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.car import car, Car
from model.util import Util
from model.client import Client
from model.engineer import Engineer

# Search for engineer device with matched mac address
def start_searching():
    global engineer
    engineer = Engineer()
    if engineer.mac_address != "invalid":
        Util.log_messages("bluetooth_start")
        if Car.detect_device(engineer.mac_address):
            engineer_menu(engineer)
        else:
            Util.log_messages("bluetooth_stop")
    else:
        Util.log_messages("no_maintainance")

def engineer_menu(engineer):
    done = False
    Util.log_messages("car_unlocked") 
    while not done: 
        Util.log_messages("engineer_menu") 
        option = Util.get_input("Option: ").lower().strip()
        if option == "q":  
            done = engineer.close_ticket()
        elif option == "l":
            print("Car locked !")
            break

if __name__ == "__main__":
    start_searching()
