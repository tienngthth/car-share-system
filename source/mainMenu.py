import sys
from model.util import Util 
from customerMenu import login_menu
from bluetoothDetect import start_searching

def main_menu():
    while True:
        print("Welcome to Car Share. Are you a:")
        print("Input C for Customer")
        print("Input E for Engineer")
        while True:  
            option = Util.get_input("Option: ").lower().strip()
            if option == "C":  
                login_menu()
            elif option == "E":  
                start_searching()

if __name__ == "__main__":
    main_menu()
