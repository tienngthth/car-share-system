import sys
from model.util import Util 
from model.account import Account
from model.car import car
from model.client import Client
from model.localDatabase import LocalDatabase
from facialScanner import start_scanning

def login_menu():
    escape = False
    while not escape:
        Util.log_messages("login_menu")
        escape = authenticate()
    
def authenticate():
    username = get_input()
    if username == "escape":
        Util.log_messages("back_to_main")
        return True
    elif username == "invalid":
        Util.log_messages("incorrect_credential")
    else:
        return customer_menu(username)

def get_input():
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "e":
            return "escape"
        if option == "f" or option == "c":
            username = start_scanning() if option == "f" else get_user_name_input()
            return verify_password(username, password = get_password_input()):

def get_user_name_input():
    username = Util.get_input("\nUsername (contains 6-15 alphanumerical characters): ")
    while not Account.validate_username(username):
        username = Util.get_input("\nInvalid username input\n\nUsername: ")
    return username

def get_password_input():
    password = Util.get_password(
        "\nPassword (contains at least 8 characters, 1 upper case, " +
        "1 lower case, 1 digit, 1 special character): "
    )
    while not Account.validate_password_input(password):
        password = Util.get_password("\nInvalid password input\n\nPassword: ")
    return password

def verify_password(username, password):
    if car.first_login:
        if verify_credential_with_mp(username, password) == "invalid":
            username == "invalid" 
    elif not Account.verify_credential_locally(username, password):
        username == "invalid" 
    return username

def create_credential_message_to_mp(username, password):
    return {
        "message_type":"credential",
        "username": username,
        "password": password,
        "user_type":"customers"
    }

# speak to MP to verify password
def verify_credential_with_mp(username, password):
    client = Client()
    encrypted_password = wait_for_response(client, create_credential_message_to_mp())
    if response != "invalid":
        first_login_to_car(username, encrypted_password)
    return response

def wait_for_response(client, message):
    client.send_message(str(message))
    while True:
        message = client.receive_message()
        if message != "":
            client.send_message("end")
            return message

def first_login_to_car(username, encrypted_password):
    car.first_login_to_car()
    LocalDatabase.insert_record("Credential", "((?), (?))",(username, encrypted_password))

def customer_menu(username):
    Util.log_messages("customer_menu")
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "l":  
            Util.log_messages("car_locked")
            return False
        elif option == "r": 
            return_car(username)
            return True

def return_car(username):
    car.return_car()
    LocalDatabase.delete_record("Credential", " WHERE Username = (?)", (username,))

if __name__ == "__main__":
    #check car status (available?)
    login_menu()