import re
from account import Account

class Customer(Account):
    def __init__(self, id, username, password, email, first_name, last_name):
        super().__init__(id, username, password, email, first_name, last_name)



