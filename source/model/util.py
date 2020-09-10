import sys, getpass
from termios import tcflush, TCIFLUSH
from time import sleep

"""
Class Util is use to handle simple function that are used accross all applications.
"""
class Util:
    #Get input from CLI
    @staticmethod
    def get_input(message):
        tcflush(sys.stdin, TCIFLUSH)
        return input(message)

    #Get input from CLI
    @staticmethod
    def get_password(message):
        tcflush(sys.stdin, TCIFLUSH)
        return getpass.getpass(prompt = message)

    @staticmethod
    def log_messages(message, parameters = None):
        if message == "main_menu":
            print("\nMain menu:")
            print("If you are a Customer: Press key \"C\"")
            print("If you are an Engineer: Press key \"E\"")
        elif message == "login_menu":
            print("\nWelcome to Car Share. Please select your login preference:")
            print("By credential: Press key \"C\"")
            print("By Facial: Press key \"F\"")
            print("To Escape: Press key \"E\"")
        elif message =="customer_menu":
            print("\nWelcome "+ parameters[0] + "! Application menu:")
            print("Lock car: Press key \"L\"")
            print("Return car: Press key \"R\"")
        elif message == "engineer_menu":
            print("\nEngineer menu:")
            print("Lock car: Press key \"L\"")
            print("Close backlog (scan QR code): Press key \"Q\"")
        elif message == "incorrect_credential":
            print("\nYou have entered incorrect username or password.")
        elif message == "back_to_main":
            print("\nGoodbye!")
        elif message == "car_locked":
            print("\nCar locked!")
        elif message == "car_unlocked":
            print("\nCar unlocked!")
        elif message == "car_returned":
            print("\nCar returned!")
        elif message == "bluetooth_start":
            print("\nSearching for engineer...")
        elif message == "bluetooth_stop":
            print("\nNo engineer found. Stop searching.")
        elif message == "no_maintainance":
            print("\nNo maintanance needed.")
        elif message == "server_connection":
            print("\nCan not connect to server.")
        elif message == "server_socket":
            print("\nCan not set up socket.")
        elif message == "facial_error":
            print("\nFacial scanner error")
        elif message == "backlog_closed":
            print("\nBacklog closed! Car locked!")
        elif message == "car_not_registered":
            print("\nThis car is not registered!")
        elif message == "wrong_code":
            print("\nInvalid code!")

    