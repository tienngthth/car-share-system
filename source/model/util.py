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
    def paginatedDisplay(recordList, page, maximum_record_per_page = 5):
        indices = Util.getIndices(len(recordList), page, maximum_record_per_page)
        return recordList[indices[0]: indices[1]]
    
    @staticmethod
    def getIndices(listSize, page, maximum_record_per_page):
        if (page == 0):
            return (0, listSize)
        firstIndex = (page - 1) * maximum_record_per_page
        if (listSize < firstIndex or page <= 0):
            return (0, 0)
        lastIndex = firstIndex + maximum_record_per_page
        if (listSize < lastIndex):
            lastIndex = listSize
        return (firstIndex, lastIndex)

    @staticmethod
    def log_messages(message):
        if message == "main_menu":
            print("\nMain menu")
            print("Input C if you are a Customer")
            print("Input E if you are an Engineer")
        elif message == "login_menu":
            print("\nWelcome to Car Share. Please select your login preference.")
            print("Input C for Credential")
            print("Input F for Facial")
            print("Input E for Escape")
        elif message =="customer_menu":
            print("\nWelcome "+ username + "! Application menu")
            print("Lock car: Press key \"L\"")
            print("Return car: Press key \"R\"")
        elif message == "incorrect_credential":
            print("\nYou have entered incorrect username or password.")
        elif message == "back_to_main":
            print("\nGoodbye!")
        elif message == "car_locked":
            print("\nCar locked!")
        elif message == "car_returned":
            print("\nCar returned!")
        elif message == "bluetooth_start":
            print("\nSearching for engineer...")
        elif message == "bluetooth_stop":
            print("\nNo engineer found. Stop searching")
        elif message == "no_maintainance":
            print("\nNo maintanance needed")
        elif message == "engineer_menu":
            print("\nCar Unlocked! Application menu")
            print("Lock car: Press key \"L\"")
            print("Close backlog (scan QR code): Press key \"C\"")