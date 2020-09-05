from bluetoothDelect import start_searching
from model import car

def engineer_menu():
    print("Application menu")
    print("1. Scan QR Code")

def customer_menu():
    print("Application menu")
    print("Lock car")
    print("Return car")

def login_menu():
    print("Welcome to Car Share")
    print("Username: ")
    print("Password: ")

if __name__ == "__main__":
    while True:
        login_menu()