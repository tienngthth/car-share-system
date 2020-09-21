import re, requests
from passlib import hash
from abc import ABC, ABCMeta, abstractmethod
from model.localDatabase import LocalDatabase
from .util import Util

"""
Account class is use to pass all the user credential, information during the booking session
"""
class Account():
    username_regex = "^[A-Za-z0-9]{6,15}$"
    passwod_regex = "^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$"

    @staticmethod
    def hash_salt_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_credential(input_password, encrypted_password):
        try:
            return hash.sha256_crypt.verify(input_password, encrypted_password)
        except:
            return False

    @staticmethod
    def verify_credential_locally(username, input_password):
        try:
            encrypted_password = LocalDatabase.select_a_record_parameterized(
                "Password", 
                "Credential", 
                " WHERE Username = (?)", 
                (username,)
            )[0]
            return Account.verify_credential(input_password, encrypted_password)
        except:
            return False
        
    @staticmethod
    def validate_username_input(username):
        return re.search(Account.username_regex, username)

    @staticmethod
    def validate_password_input(password):
        """ Valid password contains at least:
            8 characters, 1 upper case, 1 lower case,
            1 digit, 1 special characters
        """
        return not re.search(Account.passwod_regex, password)

    @staticmethod
    def get_user_name_input():
        username = Util.get_input("\nUsername (contains 6-15 alphanumerical characters): ")
        while not Account.validate_username_input(username):
            username = Util.get_input("\nInvalid username input\n\nUsername: ")
        return username

    @staticmethod
    def get_password_input():
        password = Util.get_password(
            "\nPassword (contains at least 8 characters, 1 upper case, " +
            "1 lower case, 1 digit, 1 special character): "
        )
        while not Account.validate_password_input(password):
            password = Util.get_password("\nInvalid password input\n\nPassword: ")
        return password