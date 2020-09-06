import re, requests
from account import Account
from database import Database

class Customer(Account):
    #Log to the database
    def log_data_to_db(self):
        resp = requests.get(
            "http://127.0.0.1:8080/customers/create?" + 
            "username=" + self.username + 
            "&password=" + self.password +
            "&first_name=" + self.first_name +
            "&last_name=" + self.last_name + 
            "&phone=" + self.phone +
            "&email=" + self.email
        )
        print(resp.text)

# #Test create new account with encrypted password
customer = Customer("ABC", "123abc", "abc@abc", "Tien", "Nguyen", "1234567", "customer")
customer.log_data_to_db()