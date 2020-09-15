import re, requests
from passlib import hash
from abc import ABC, ABCMeta, abstractmethod

class Account(ABC):
    def __init__(self, username, password, email, firstname, lastname, phone):
        super().__init__()
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone        

    def validate_new_account(self):
        if not Account.validate_username_input(self.username):
            return "Incorrectly formatted username or already existed username"
        elif not Account.validate_password_input(self.password):
            return "Invalid formatted password"
        elif not Account.validate_email_input(self.email):
            return "Invalid formatted email"
        elif not Account.validate_phone_input(self.phone):
            return "Invalid formatted phone"
        requests.post(
            "http://127.0.0.1:8080/customers/create?" +
            "username=" + self.username +
            "&password=" + self.hash_salt_password(self.password) +
            "&first_name=" + self.firstname +
            "&last_name=" + self.lastname +
            "&email=" + self.email +
            "&phone=" + self.phone
        )
        return "Valid"

    @staticmethod
    def hash_salt_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_password(username, input_password):
        try:
            user = requests.get(
                "http://127.0.0.1:8080/get/user/info?username=" +
                username
            ).json()
            if hash.sha256_crypt.verify(input_password, user["Password"]):
                return user
            else: 
                return "invalid"
        except:
            return "invalid"

    @staticmethod
    def validate_username_input(username):
        # Valid username is unique and contains 6-15 alphanumerical characters 
        existed_username = requests.get(
            "http://127.0.0.1:8080/customers/check/existed/username?username=" 
            + username
        ).text == "0"
        return existed_username and re.search("^[A-Za-z0-9]{6,15}$", username) and username != "invalid"

    @staticmethod
    def validate_password_input(password):
        """ Valid password contains at least:
            8 characters, 1 upper case, 1 lower case,
            1 digit, 1 special characters
        """
        return not re.search("^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$", password)

    @staticmethod
    def validate_email_input(email):
        """ Valid email input: 
            1. Before "@", minimum length of the text (between 2 dots/underscors) is 2. 
            Has to start with/end with/contain only alphanumerical characters.
            2. After "@", requires 2 alphabetical text with a "." between. 
            The latter contains 2 to 3 characters.
        """
        return re.search("^([A-Za-z0-9]+([.]|[_])?[A-Za-z0-9]+)+[@][A-Za-z]+[.][A-Za-z]{2,3}$", email)

    @staticmethod      
    def validate_phone_input(phone):
        # Valid phone contains at least 5 characters, all is numbers
        return re.search("^[0-9]{5,}$", phone)