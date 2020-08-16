import bluetooth
import socket
from .util import Util

"""
Class Server is to create instances to send context messages and accept connection request
Base on RFCOMM protocol and bluetooth package, create client using socket programming
"""

class Server:
    def __init__(self, host = '', port = 6):
        self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.__set_up_connection(host, port)
        self.__connection = None
        self.__accept_connection()

    #Open socket and bind socket to a physical port (default is port 6)
    def __set_up_connection(self, host, port):
        self.__socket.bind((host, port))
        self.__socket.listen(1) 
        print("Listening...")  

    #Accept connection
    def __accept_connection(self):
        self.__connection, addr = self.__socket.accept()
        self.send_message("Server has connected to this client\n")

    #Send message
    def send_message(self, message):
        self.__connection.send(message)

    #Retrieve and decode the latest message
    def retrieve_message(self):
        return self.__socket.recv(1024).decode('UTF-8')

    def __close_socket(self):
        self.__socket.close()

    def close_connection(self):
        self.__close_socket()
        self.__connection.close() 

    