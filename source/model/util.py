import sys, getpass
# from termios import tcflush, TCIFLUSH
from time import sleep

"""
Class Util is use to handle simple function that are used accross all applications.
"""
class Util:
    #Get input from CLI
    @staticmethod
    def get_input(message):
        # tcflush(sys.stdin, TCIFLUSH)
        return input(message)

    #Get input from CLI
    @staticmethod
    def get_password(message):
        # tcflush(sys.stdin, TCIFLUSH)
        return getpass.getpass(prompt = message)