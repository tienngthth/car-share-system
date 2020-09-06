import keyboard, sys, msvcrt, getpass
from model.util import Util 
from model.account import Account
# from termios import tcflush, TCIFLUSH

def customer_menu():
    print("Application menu")
    print("Lock car: Press key \"L\"")
    print("Return car: Press key \"R\"")
    while True:  # making a loop
        # tcflush(sys.stdin, TCIFLUSH)
        if keyboard.is_pressed('l'):  # if key 'q' is pressed 
            print('Car locked!\n')
            break
        elif keyboard.is_pressed('r'):
            print('Car returned!\n')
            sys.exit()  

def login_menu():
    while True:
        print("Welcome to Car Share")
        if Account.verify_password(get_user_name_input(), get_password_input(), "customers"):
            customer_menu()
        else:
            print("You have entered incorrect username or password.\n")

def get_user_name_input():
    username = Util.get_input("Username (contains 6-15 alphanumerical characters): ")
    # while not Account.validate_username(username):
    #     username = Util.get_input("Invalid username input\nUsername: ")
    return username

def get_password_input():
    password = Util.get_password(
        "Password (contains at least 8 characters, 1 upper case, " +
        "1 lower case, 1 digit, 1 special character): "
    )
    # while not Account.validate_password_input(password):
        # password = Util.get_password("Invalid password input\nPassword: ")
    return password

if __name__ == "__main__":
    login_menu()