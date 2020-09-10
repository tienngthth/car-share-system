from .client import Client
from .util import Util

class Car:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Car.__instance == None:
            Car()
        return Car.__instance

    def __init__(self, first_login = True, ap_addr = "DC:A6:32:4A:0C:41"):
        """ Virtually private constructor. """
        if Car.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Car.__instance = self
            self.__ap_addr = ap_addr
            self.__first_login = first_login

    def first_login_to_car(self):
        self.first_login = False
        self.__change_car_status("In use")

    def return_car(self):
        Util.log_messages("car_returned")
        self.first_login = True
        self.__change_car_status("Available")

    #speak to MP to change car status to available
    def __change_car_status(self, status):
        client = Client()
        car_status_message = {
            "message_type":"car_status",
            "ap_addr":self.__ap_addr,
            "car_status":status
        }
        client.send_message(str(car_status_message))
        client.send_message("end")

    @property
    def first_login(self):
        return self.__first_login

    @first_login.setter
    def first_login(self, first_login):
        self.__first_login = first_login

    @property
    def ap_addr(self):
        return self.__ap_addr

car = Car()

