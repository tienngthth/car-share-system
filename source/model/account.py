import re
from passlib import hash
from abc import ABC, ABCMeta, abstractmethod

class Account(ABC):
    def __init__(self, id, username, password, email, first_name, last_name):
        super().__init__()
        self.__username = username
        self.__password = Account.hash_salt_password(password)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__id = id

    @staticmethod
    def hash_salt_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_password(input_password, username):
        #retrieve password from database by username
        encryptedPassword = ""
        return hash.sha256_crypt.verify(input_password, encryptedPassword)

    @staticmethod
    def validate_username_input(username):
        # Valid username is unique and contains 6-15 alphanumerical characters 
        existed_username = True     #Need to check from the database
        if existed_username and re.search("^[A-Za-z0-9]{6,15}$", username): 
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

    @staticmethod
    def validate_email_input(email):
        """ Valid email input: 
            1. Before "@", minimum length of the text (between 2 dots/underscors) is 2. 
            Has to start with/end with/contain only alphanumerical characters.
            2. After "@", requires 2 alphabetical text with a "." between. 
            The latter contains 2 to 3 characters.
        """
        if re.search("^([A-Za-z0-9]+([.]|[_])?[A-Za-z0-9]+)+[@][A-Za-z]+[.][A-Za-z]{2,3}$", email):
            return True
        return False
