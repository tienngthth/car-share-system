import re
from account import Account
from database import Database

class Customer(Account):
    def __init__(self, username, password, email, first_name, last_name):
        super().__init__(username, password, email, first_name, last_name, "customer")

    #Login to the database
    def __log_data_to_db(self):
        try:
            parameters = (
                self.__username, self.__password, 
                self.__first_name, self.__last_name, 
                self.__email
            )
            Database.insert_record(
                "Staff (Username, Password, FirstName, LastName, Email)",
                "(%s, %s, %s, %s, %s)",
                parameters
            )
        except:
            pass