from .camera import Camera
from .client import Client
from .util import Util
from .account import Account
from .facialScanner import FacialScanner
from .localDatabase import LocalDatabase
from .car import car

class Customer():    
    def __init__(self, option):
        self.__username = "invalid"
        self.__password = "invalid"
        self.__get_credential()  

    def __get_crendential(self):
        if option == "f":
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
        self.password = self.__get_encrypted_password_from_mp(client)
        if self.password != "invalid":
            self.__first_login_to_car()
        return self.password

    def __get_encrypted_password_from_mp(self, client):
        client.send_message(str(self.__get_credential_message_to_mp()))
        while True:
            message = client.receive_message()
            if message != "":
                client.send_message("end")
                return message

    def __get_credential_message_to_mp(self):
        return {
            "message_type":"credential",
            "username": self.username,
            "password": self.password,
            "user_type":"customers"
        }

    def __first_login_to_car(self):
        car.first_login_to_car()
        LocalDatabase.insert_record("Credential", "((?), (?))",(self.username, self.password))

    def return_car(self):
        car.return_car()
        LocalDatabase.delete_record("Credential", " WHERE Username = (?)", (self.username,))

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
