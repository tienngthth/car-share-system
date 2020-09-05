class Car:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Car.__instance == None:
            Car()
        return Car.__instance

    def __init__(self, available_status = None, lock_status = None, ap_addr = None):
        """ Virtually private constructor. """
        if Car.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Car.__instance = self
            self.__ap_addr = ap_addr
            self.__available_status = available_status
            self.__lock_status = lock_status

    @property
    def available_status(self):
        return self.__available_status

    @available_status.setter
    def available_status(self, available_status):
        self.__available_status = available_status

    @property
    def lock_status(self):
        return self.__lock_status

    @lock_status.setter
    def lock_status(self, lock_status):
        self.__lock_status = lock_status

car = Car()

