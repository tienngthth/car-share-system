import re
from passlib import hash
from abc import ABC, ABCMeta, abstractmethod

class Account(ABC):
    def __init__(self, username, password, first_name, last_name):
        super().__init__()
        self.__username = username
        self.__password = Account.hash_password(password)
        self.__first_name = first_name
        self.__last_name = last_name

    @staticmethod
    def hash_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_password(input_password, username):
        #retrieve password from database by username
        hashedPassword = ""
        return hash.sha256_crypt.verify(input_password, hashedPassword)

    @staticmethod
    def validate_username_input(username):
        # Valid username contains at least 6 characters, all is alphanumerical characters
        if re.search("^[A-Za-z0-9]{6,}$", username):
            return True
        return False

    @staticmethod
    def validate_password_input(password):
        """ Valid password contains at least:
            8 characters, 1 upper case, 1 lower case,
            1 digit, 1 special characters
        """
        if re.search("^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$", password):
            return False
        else:
            return True 
