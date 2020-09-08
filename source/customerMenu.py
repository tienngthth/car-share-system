import sys
from model.util import Util 
from model.account import Account
from model.car import car
from model.client import Client
from model.localDatabase import LocalDatabase
from facialScanner import start_scanning

def login_menu():
    global escape
    escape = False
    while not escape:
        print("\nWelcome to Car Share. Please select your login preference.")
        print("Input C for Credential")
        print("Input F for Facial")
        print("Input E for Escape")
        authenticate()
    print("\nGoodbye!")

def authenticate():
    global escape
    username = get_input()
    if username == "Escape":
        escape = True
    elif username == "Invalid":
        print("\nYou have entered incorrect username or password.")
    else:
        customer_menu(username)

def get_input():
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "f":  
            return facial_login()
        elif option == "c":  
            return credential_login()
        elif option == "e":
            return "Escape"

def facial_login():
    username = start_scanning()
    if car.first_login:

        car.first_login_to_car()
    if username == LocalDatabase.select_a_record("Username", "Credential")[0]:
        if car.first_login:
            car.first_login_to_car()
            #ask for full credentail and save back to local db
        return username
    else: 
        return "Invalid"

def credential_login():
    username = get_user_name_input()
    password = get_password_input()
    if verify_password(username, password):
        return username
    else:
        return "Invalid"

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
    # speak to MP to verify password
        if verify_password_first_login(username, password):
            car.first_login_to_car()
            return True
    else:
        # talk to local dabase to verify credential
        return verify_password_locally(username, password, "credential") 
    return False

def verify_password_first_login(username, authentication_type, password):
    client = Client()
    credential_message = {
        "message_type":"credential",
        "username":username,
        "password":password,
        "user_type":"customers"
    }
    if wait_for_response(client, credential_message):
        LocalDatabase.update_last_record(
            "Credential", "Username, Password",
            (username, Account.hash_salt_password(password))
        )
        return True
    return False

def wait_for_response(client, credential_message):
    client.send_message(str(credential_message))
    while True:
        message = client.receive_message()
        if message != "":
            client.send_message("end")
            return True if message == "valid" else False

def verify_password_locally(username, password):
    valid_crendential = LocalDatabase.select_a_record("*", "Credential")[0]
    if username == valid_crendential[0]:
        if Account.hash_salt_password(password) == valid_crendential[1]:
            return True
    return False

def customer_menu(username):
    global escape
    print("\nWelcome "+ username + "! Application menu")
    print("Lock car: Press key \"L\"")
    print("Return car: Press key \"R\"")
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "l":  
            print("\nCar locked!")
            break
        elif option == "r": 
            escape = True 
            car.return_car()
            break

if __name__ == "__main__":
    #check car status (available?)
    login_menu()
