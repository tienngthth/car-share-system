import pymysql, datetime, timedelta
import connect

def selectFromCustomer(cursor):
    print("Customer table:")
    cursor.execute("SELECT * FROM Customer")
    for x in cursor:
        print(x)

def selectFromStaff(cursor):
    print("Staff table:")
    cursor.execute("SELECT * FROM Staff")
    for x in cursor:
        print(x)

def selectFromCar(cursor):
    print("Car table:")
    cursor.execute("SELECT * FROM Car")
    for x in cursor:
        print(x)

def selectFromBooking(cursor):
    print("Booking table:")
    cursor.execute("SELECT * FROM Booking")
    for x in cursor:
        print(x)

def selectFromBacklog(cursor):
    print("Backlog table:")
    cursor.execute("SELECT * FROM Backlog")
    for x in cursor:
        print(x)

def executeQueries():
    #Connect to the database
    cursor = connect.connectToDatabase().cursor()
    #Retrieve all data
    selectFromCustomer(cursor)
    selectFromStaff(cursor)
    selectFromCar(cursor)
    selectFromBooking(cursor)
    selectFromBacklog(cursor)
    print("Done")

executeQueries()