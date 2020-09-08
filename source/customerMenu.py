import sys
from termios import tcflush, TCIFLUSH
from model.util import Util 
from model.account import Account
from model.car import car
from model.client import Client
from facialScanner import start_scanning

def login_menu():
    while True:
        print("Welcome to Car Share. Please select your login preference.")
        print("Input C for Credential")
        print("Input F for Facial")
        username = authenticate()
        ## car repaired? -> kcho vao
        if username != "Invalid":
            customer_menu(username)
        else:
            print("You have entered incorrect username or password.\n")

def authenticate():
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "f":  
            return facial_login()
        elif option == "c":  
            return credential_login()

def facial_login():
    start_scanning()
    return "Invalid"

def credential_login():
    username = get_user_name_input()
    password = get_password_input()
    if verify_password(username, password):
        return username
    else:
        return "Invalid"

def get_user_name_input():
    username = Util.get_input("Username (contains 6-15 alphanumerical characters): ")
    while not Account.validate_username(username):
        username = Util.get_input("Invalid username input\nUsername: ")
    return username

def get_password_input():
    password = Util.get_password(
        "Password (contains at least 8 characters, 1 upper case, " +
        "1 lower case, 1 digit, 1 special character): "
    )
    while not Account.validate_password_input(password):
        password = Util.get_password("Invalid password input\nPassword: ")
    return password

def verify_password(username, password):
    if car.first_login:
    # speak to MP to verify password
        if verify_password_first_login(username, password):
            car.first_login_to_car()
            #need to reset credential in local database
            return True
    elif False: # talk to local dabase to verify
        return True
    return False

def verify_password_first_login(username, password):
    client = Client()
    credential_message = {
        "message_type":"credential",
        "username":username,
        "password":password,
        "user_type":"customers"
    }
    client.send_message(str(credential_message))
    return wait_for_response(client)

def wait_for_response(client):
    while True:
        message = client.receive_message()
        if message != "":
            client.send_message("end")
            return True if message == "valid" else False

def customer_menu(username):
    print("Welcome "+ username + "! Application menu")
    print("Lock car: Press key \"L\"")
    print("Return car: Press key \"R\"")
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "l":  
            print('Car locked!\n')
            break
        elif option == "r":  
            car.return_car()
            break

if __name__ == "__main__":
    #check car status (available?)
    login_menu()
