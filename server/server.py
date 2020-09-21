#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server.py
====================================
Class Server is to create instances to send context messages and accept connection request
Base on socket protocal and package, create client using socket programming
Socket documentation: https://docs.python.org/3/library/socket.html
"""
import socket, sys

class Server:
    """
    Define the port and interface to listen on, then open the socket.
    """
    #Initialize instance
    def __init__(self, host = '10.247.169.92', port = 9956):
        self.__address = (host, port)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__set_up_connection()
        self.__connection = None
        self.__accept_connection()

    #Open socket and bind socket to a physical port (default is port 6)
    def __set_up_connection(self):
        try:
            self.__socket.bind(self.__address)
            self.__socket.listen()
        except:
            print("\nCan not set up socket.")
            sys.exit()

    #Accept connection
    def __accept_connection(self):
        """
        Accept inbound connections
        """
        print("Listening on {}...".format(self.__address))
        self.__connection, client_address = self.__socket.accept()
        print("Connected to {}".format(client_address))

    #Send message
    def send_message(self, message):
        """
        Return a message to a connected client thath as made a request. Parameters:
        message: The message to return. Will be encoded UTF-8.
        """
        self.__connection.sendall(message.encode('utf-8'))

    #Retrieve and decode the latest message
    def receive_message(self):
        """
        Retrieve and decode the latest message (assumes UTF-8).
        """
        return self.__connection.recv(1024).decode('utf-8')

    #End connection
    def close_connection(self):
        """
        Close an open connection.
        """
        self.__connection.close()
        self.__accept_connection()
