import bluetooth
from time import sleep
from .util import Util

"""
Class Client is to create instances to send connect request and receive context message
Base on RFCOMM protocol and bluetooth package, create client using socket programming
"""

class Client:
   #Initialize instance
   def __init__(self, port = 6, server_name = None, server_mac_address = None):
      #Create socket
      self.__port = port
      self.__find_server(server_name, server_mac_address)
      self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
      self.__open_socket()

   #Let user input server name or use default name
   def __find_server(self, server_name, server_mac_address):
      
      #Prioritize Mac address over server name if both is presented
      if server_mac_address is None and server_name is None:
         Util.raise_error("Please input server name or server mac address")
      if server_mac_address is not None and server_name is not None:
         print("Server mac address is used")
      print("Finding server...")

      #Use default value of server name and Mac address
      if server_mac_address is not None:
         self.__server_mac_address = server_mac_address
      else:
         self.__server_mac_address = self.__search(server_name)

   # Search for device based on device's name
   def __search(self, server_name):
      for i in range(5):
         sleep(3) #Sleep three seconds 
         nearby_devices = bluetooth.discover_devices()

         for server_mac_address in nearby_devices:
               if server_name == bluetooth.lookup_name(server_mac_address, timeout = 5):
                  return server_mac_address
      Util.raise_error("Can not detect specified nearby device")

   #Try to create a connection
   def __open_socket(self):
      try:
         self.__socket.connect((self.__server_mac_address, self.__port))
      except:
         Util.raise_error("Can not connect to specified server")


   #Send message to server
   def send_message(self, message):
      self.__socket.send(message)

   #Retrive the last message that server send. If all messages have been read, the function will return empty string
   def retrieve_message(self):
      return self.__socket.recv(1024).decode('UTF-8')

   #End connection and close the socket to reuse the port for different purposes
   def close_socket(self):
      self.__socket.close()
