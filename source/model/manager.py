import re
from account import Account

class Manager(Account):
    def __init__(self, username, password, email, first_name, last_name):
        super().__init__(username, password, email, first_name, last_name, "Manager")




