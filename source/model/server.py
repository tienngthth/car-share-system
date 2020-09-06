"""# !/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html"""
import socket

"""
Class Server is to create instances to send context messages and accept connection request
Base on socket protocal and package, create client using socket programming
"""

class Server:
    #Initialize instance
    def __init__(self, host = '127.0.0.1', port = 9985):
        self.__address = (host, port)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__set_up_connection()
        self.__connection = None
        self.__accept_connection()

    #Open socket and bind socket to a physical port (default is port 6)
    def __set_up_connection(self):
        self.__socket.bind(self.__address)
        self.__socket.listen() 
        print("Listening on {}...".format(self.__address))  

    #Accept connection
    def __accept_connection(self):
        self.__connection, client_address = self.__socket.accept()
        print("Connected to {}".format(client_address))
      
    #Send message
    def send_message(self, message):
        self.__connection.sendall(message.encode('utf-8'))

    #Retrieve and decode the latest message
    def receive_message(self):
        return self.__connection.recv(1024).decode('utf-8')

    #End connection
    def close_connection(self):
        self.__socket.close()
        self.__connection.close()
