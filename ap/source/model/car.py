import sys, bluetooth
from time import sleep
from .client import Client
from .util import Util
from .code import Code

"""
This class is a singleton to handle and pass all the car information throughout the program
"""
class Car:
    __instance = None

    def __init__(self, first_login = True, ap_addr = "DC:A6:32:4A:0C:41"):
        """ Virtually private constructor. """
        if Car.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Car.__instance = self
            self.__ap_addr = ap_addr
            self.__first_login = first_login
            self.__car_id = None
            self.__booking_id = None
            self.__get_car_id()

    def __get_car_id(self):
        client = Client()
        message = {"message_type":"get_car_id", "ap_addr":self.__ap_addr}
        client.send_message(str(message))
        while True:
            message = client.receive_message()
            if message != "":
                client.send_message("end")
                if message == "invalid":
                    Util.log_messages("car_not_registered")
                    sys.exit()
                self.car_id = int(message)
                break

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Car.__instance == None:
            Car()
        return Car.__instance

    @staticmethod 
    def detect_device(device_mac_address):
        # Wait until bluetooth is on and stable (loop throught the unstable period)
        for i in range(1):         
            try:
                sleep(2)   
                # Get all nearby devices mac address
                nearby_devices_mac_address = bluetooth.discover_devices()
                # Loop through all nearby devices
                for mac_address in nearby_devices_mac_address:
                    if mac_address == device_mac_address:
                        return True
            except:
                Car.detect_device(device_mac_address)
        return False

    def first_login_to_car(self):
        self.first_login = False

    def return_car(self):
        Util.log_messages("car_returned")
        self.first_login = True
        self.booking_id = None
        self.__change_car_status("Available")

    #speak to MP to change car status to available
    def __change_car_status(self, status):
        client = Client()
        car_status_message = {
            "message_type":"update_car_status",
            "car_id": self.car_id,
            "car_status":status
        }
        client.send_message(str(car_status_message))
        while True:
            message = client.receive_message()
            if message != "":
                client.send_message("end")
                break
        client.send_message("end")

    def get_assgined_engineer_info(self):
        client = Client()
        message = {"message_type" : "check_backlog", "car_id" : self.car_id}
        client.send_message(str(message))
        while True:
            message = client.receive_message()
            if message != "":
                if message != "invalid":
                    message = Code.parse_json(message.replace("\'", "\""))
                client.send_message("end")
                return message

    @property
    def first_login(self):
        return self.__first_login

    @first_login.setter
    def first_login(self, first_login):
        self.__first_login = first_login

    @property
    def ap_addr(self):
        return self.__ap_addr

    @ap_addr.setter
    def ap_addr(self, ap_addr):
        self.__ap_addr = ap_addr

    @property
    def car_id(self):
        return self.__car_id

    @car_id.setter
    def car_id(self, car_id):
        self.__car_id = car_id
  
    @property
    def booking_id(self):
        return self.__booking_id

    @booking_id.setter
    def booking_id(self, booking_id):
        self.__booking_id = booking_id

# car = Car()

