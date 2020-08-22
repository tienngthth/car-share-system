import datetime
import json

class Code():
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.decoded_content = Code.decode_content(raw_data)
        self.__time_stamp = datetime.datetime.now()

    @staticmethod
    def decode_content(raw_data):
        return raw_data.data.decode("utf-8")

    @staticmethod
    def parse_json(content):
        return json.load(content)

    #Getters and setters
    @property
    def decoded_content(self):
        return self.__decoded_content

    @decoded_content.setter
    def decoded_content(self, decoded_content):
        self.__decoded_content = decoded_content