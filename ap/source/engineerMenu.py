#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model.car import car, Car
from model.util import Util
from model.client import Client
from model.engineer import Engineer

"""
This file work to run on the logic flow of the engineer which will unlock the car by bluetooth and other operation after the car is unlocked
"""
# Search for engineer device with matched mac address
def start_searching():
    global engineer
    engineer = Engineer()
    if engineer.engineer_info != "invalid":
        Util.log_messages("bluetooth_start")
        if Car.detect_device(engineer.mac_address):
            engineer_menu(engineer)
        else:
            Util.log_messages("bluetooth_stop")
    else:
        Util.log_messages("no_maintainance")


"""
This menu will displayed after AP detect engineer and unlock the car
"""
def engineer_menu(engineer):
    """
    The menu have 2 options: log the car (can still log back in) and scan QR code (lock the car and fix all the backlogs of that car)
    """
    done = False
    Util.log_messages("car_unlocked") 
    while not done: 
        Util.log_messages("engineer_menu") 
        option = Util.get_input("Option: ").lower().strip()
        if option == "q":  
            if engineer.scan_code() and confirm_close_backlog():
                break
        elif option == "l":
            Util.log_messages("car_locked")
            break

"""
Display a confirmation with the engineer to close all backlog
"""
def confirm_close_backlog():
    Util.log_messages("close_backlog_confirm")
    option = Util.get_input("Option: ").lower().strip()
    if option == "y":  
        engineer.close_backlog()
        return True
    return False


if __name__ == "__main__":
    start_searching()
