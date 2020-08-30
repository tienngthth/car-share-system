import re
from account import Account
from database import Database

class Customer(Account):
    def __init__(self, username, password, email, first_name, last_name, phone):
        super().__init__(username, password, email, first_name, last_name, phone, "customer")
