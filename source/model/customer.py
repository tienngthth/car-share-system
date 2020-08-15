import re
from account import Account

class Customer(Account):
    def __init__(self, username, password, email, phone):
        super().__init__(username, password)
        self.__email = email
        self.__phone = phone

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

