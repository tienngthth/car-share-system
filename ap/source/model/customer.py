from .camera import Camera
from .client import Client
from .util import Util
from .account import Account
from .facialScanner import FacialScanner
from .localDatabase import LocalDatabase
from .car import car
from .code import Code

class Customer():    
    def __init__(self, get_username_option):
        self.__username = "invalid"
        self.__password = "invalid"
        self.__booking_id = None
        self.__get_credential(get_username_option)  

    def __get_credential(self, get_username_option):
        if get_username_option == "f":
            self.username = FacialScanner.start_scanning() 
        else:
            self.username = Account.get_user_name_input()
        if self.username != "invalid":
            self.password = Account.get_password_input()
            self.__verify_credential()

    def __verify_credential(self):
        if car.first_login:
            if self.__verify_credential_with_mp() == "invalid":
                self.username = "invalid" 
        elif not Account.verify_credential_locally(self.username, self.password):
            self.username = "invalid" 

    # speak to MP to verify password
    def __verify_credential_with_mp(self):
        client = Client()
        message = self.__get_encrypted_password_from_mp(client)
        if message != "invalid":
            self.password = message["password"]
            self.booking_id = message["booking_id"]
            self.__first_login_to_car()
        self.password = "invalid"

    def __get_encrypted_password_from_mp(self, client):
        client.send_message(str(self.__get_credential_message_to_mp()))
        while True:
            message = client.receive_message()
            if message != "":
                client.send_message("end")
                if message != "invalid":
                    return Code.parse_json(message.replace("\'", "\""))
                return message

    def __get_credential_message_to_mp(self):
        return {
            "message_type":"credential",
            "username": self.username,
            "password": self.password,
            "car_id": car.car_id,
            "user_type":"customers"
        }

    def __first_login_to_car(self):
        car.first_login_to_car()
        LocalDatabase.insert_record("Credential", "((?), (?))",(self.username, self.password))

    def return_car(self):
        car.return_car()
        self.__done_booking()
        LocalDatabase.delete_record("Credential", " WHERE Username = (?)", (self.username,))

    def __done_booking(self):
        client = Client()
        car_status_message = {
            "message_type":"done_booking",
            "car_id":self.booking_id
        }
        client.send_message(str(car_status_message))
        client.send_message("end")

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def booking_id(self):
        return self.__booking_id

    @booking_id.setter
    def booking_id(self, booking_id):
        self.__booking_id = booking_id
