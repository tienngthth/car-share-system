"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
import re, requests
from passlib import hash
from flask import flash

class Account():
    def __init__(self, username, password, email, firstname, lastname, phone, user_id="", mac_address=""):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone      
        self.user_id = user_id      
        self.mac_address = mac_address        

    def validate_new_account(self):
        if Account.validate_username_input(self.username):
            if Account.validate_username_uniqueness(self.username):
                if Account.validate_password_input(self.password):
                    if Account.validate_email_input(self.email):
                        if Account.validate_phone_input(self.phone):
                            return True
        return False

    def register_account(self):
        requests.post(
            "http://127.0.0.1:8080/customers/create?" +
            "username=" + self.username +
            "&password=" + self.hash_salt_password(self.password) +
            "&first_name=" + self.firstname +
            "&last_name=" + self.lastname +
            "&email=" + self.email +
            "&phone=" + self.phone
        )
        flash("Account registered! Please log in.")

    def validate_update_account(self):
        if self.username != "" and not Account.validate_username_input(self.username):
            return False
        if self.username != "" and not Account.validate_username_uniqueness(self.username):
            return False
        if self.password != "" and not Account.validate_password_input(self.password):  
            return False
        if self.email != "" and not Account.validate_email_input(self.email):
            return False
        if self.phone != "" and not Account.validate_phone_input(self.phone):
            return False
        flash("Account updated!")
        return True

    def update_account(self):
        requests.put(
            "http://127.0.0.1:8080/customers/update?" +
            "username=" + self.username +
            "&password=" + self.hash_salt_password(self.password) +
            "&first_name=" + self.firstname +
            "&last_name=" + self.lastname +
            "&email=" + self.email +
            "&phone=" + self.phone +
            "&mac_address=" + self.mac_address +
            "&id=" + self.user_id
        )

    @staticmethod
    def hash_salt_password(raw_input):
        return hash.sha256_crypt.hash(raw_input)

    @staticmethod
    def verify_password(username, input_password):
        if not Account.validate_username_input(username):
            flash("Incorrectly formatted username.")
        elif not Account.validate_password_input(input_password):
            flash("Invalid formatted password")
        else:
            try:
                user = requests.get("http://127.0.0.1:8080/get/user/info?username="+username).json()
                if hash.sha256_crypt.verify(input_password, user["Password"]):
                    return user
                else:
                    flash("Invalid password or username.")
            except:
                flash("Can not verify credential.")
        return False

    @staticmethod
    def validate_username_input(username):
        if re.search("^[A-Za-z0-9_]{6,15}$", username) and username != "invalid":
            return True
        else:
            flash("Incorrectly formatted username. Valid username contains 6-15 letters.")
            return False

    @staticmethod
    def validate_username_uniqueness(username):
        customer_username_check = requests.get(
            "http://127.0.0.1:8080/customers/check/existed/username?username=" 
            + username
        ).text == "0" 
        staff_username_check = requests.get(
            "http://127.0.0.1:8080/staffs/check/existed/username?username=" 
            + username
        ).text == "0"
        if customer_username_check and staff_username_check:
            return True
        flash("Already existed username.")
        return False

    @staticmethod
    def validate_password_input(password):
        """ Valid password contains at least:
            8 characters, 1 upper case, 1 lower case,
            1 digit, 1 special characters
        """
        if not re.search("^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$", password):
            return True
        flash("Invalid formatted password. Valid password contains at least 8 characters, 1 upper case, 1 lower case, 1 digit, 1 special characters")
        return False

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
        flash("Invalid formatted email.")
        return False

    @staticmethod      
    def validate_phone_input(phone):
        # Valid phone contains at least 5 characters, all is digits
        if re.search("^[0-9]{5,}$", phone):
            return True
        flash("Invalid formatted phone.")
        return False