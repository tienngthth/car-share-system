class Car:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Car.__instance == None:
            Car()
        return Car.__instance

    def __init__(self, status = None, ap_addr = None):
        """ Virtually private constructor. """
        if Car.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Car.__instance = self
            self.__ap_addr = ap_addr
            self.__status = status

    

