import sys
from model.util import Util 
from customerMenu import login_menu
from bluetoothDetect import start_searching

def main_menu():
    while True:
        print("\nMain menu")
        print("Input C if you are a Customer")
        print("Input E if you are a Engineer")
        option = Util.get_input("Option: ").lower().strip()
        if option == "c":  
            login_menu()
        elif option == "e":  
            start_searching()

if __name__ == "__main__":
    main_menu()
