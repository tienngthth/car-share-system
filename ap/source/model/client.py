"""#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html"""
import socket, sys
from time import sleep
from .util import Util

"""
Class Server is to create instances to send context messages and accept connection request
Base on socket protocal and package, create client using socket programming
"""

class Client:
   #Initialize instance
   def __init__(self, host = '10.247.169.92', port = 9956):
      self.__address = (host, port)
      self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.__connect_socket()

   #Try to create a connection
   def __connect_socket(self):
      try:
         self.__socket.connect(self.__address)
      except:
         Util.log_messages("server_connection")
         sys.exit()

   #Send message
   def send_message(self, message):
      self.__socket.sendall(message.encode('utf-8'))
      sleep(0.1)

   #Retrieve and decode the latest message
   def receive_message(self):
      return self.__socket.recv(1024).decode('utf-8')

   #Close the socket to reuse the port for different purposes
   def close_socket(self):
      self.__socket.close()