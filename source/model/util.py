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
