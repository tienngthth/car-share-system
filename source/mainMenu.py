import sys
from model.util import Util 
from customerMenu import login_menu
from bluetoothDetect import start_searching
from model.util import Util 

def main_menu():
    while True:
        Util.log_messages("main_menu")
        option = Util.get_input("Option: ").lower().strip()
        if option == "c":  
            login_menu()
        elif option == "e":  
            start_searching()

if __name__ == "__main__":
    main_menu()
