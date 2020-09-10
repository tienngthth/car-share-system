import re, requests
from passlib import hash
from abc import ABC, ABCMeta, abstractmethod

class Account():
    def __init__(self, username, password, email, first_name, last_name, phone, user_type):
        self.username = username
        self.password = Account.hash_salt_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.user_type = user_type

    @staticmethod
    def hash_salt_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_password(username, input_password, user_type):
        #user_type == staffs/customers
        #retrieve password from database by username
        encryptedPassword = requests.get(
            "http://127.0.0.1:8080/" +
            user_type +
            "/get/encrypted/password/by/username?username=" +
            username
        ).text
        try:
            return hash.sha256_crypt.verify(input_password, encryptedPassword)
        except:
            return False

    @staticmethod
    def validate_username_input(username, user_type):
        # Valid username is unique and contains 6-15 alphanumerical characters 
        existed_username = requests.get(
            "http://127.0.0.1:8080/" +
            user_type +
            "/get/number/of/existed/username?username=" + 
            username
        ).text == "0"
        if existed_username and re.search("^[A-Za-z0-9]{6,15}$", username) and username != "invalid":
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

    @staticmethod      
    def validate_phone_input(phone):
        # Valid phone contains at least 5 characters, all is numbers
        if re.search("^[0-9]{5,}$", phone):
            return True
        return False

    @staticmethod
    def validate_email_phone_uniqueness(email, phone, user_type):
        # Valid uniqueness of email and phone combination
        return requests.get(
            "http://127.0.0.1:8080/" +
            user_type +
            "/get/number/of/existed/email/and/phone/combination?" +
            "email=" + email +
            "&phone=" + phone
        ).text == "0"

#Test validate username
print(Account.validate_username_input("tien123N", "customers"))
print(Account.validate_username_input("Tam", "customers"))

#Test verify password
print(Account.verify_password("tien123N", "123", "customers"))
print(Account.verify_password("ABC", "123abc", "customers"))

#Test uniqueness of email and phone combination
print(Account.validate_email_phone_uniqueness("thanh456@gmail.com", "12345678", "customers"))
print(Account.validate_email_phone_uniqueness("thanh456@gmail.com", "123456798", "customers"))