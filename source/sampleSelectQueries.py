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

def selectNumberOfBookingsPerDay(cursor):
    print("Number of bookings per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, COUNT(DATE(RentTime)) AS Daily_Bookings FROM Booking GROUP BY DATE(RentTime)")
    for x in cursor:
        print(x)

def selectNumberOfReturnsPerDay(cursor):
    print("Number of returns per day:")
    cursor.execute("SELECT DATE(ReturnTime) AS Date, COUNT(DATE(ReturnTime)) AS Daily_Returns FROM Booking GROUP BY DATE(ReturnTime)")
    for x in cursor:
        print(x)

def selectProfitPerDay(cursor):
    print("Profit per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, SUM(TotalCost) AS Daily_Profit FROM Booking GROUP BY DATE(RentTime)")
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
    #Additional queries (for drawing graphs)
    selectNumberOfBookingsPerDay(cursor)
    selectNumberOfReturnsPerDay(cursor)
    selectProfitPerDay(cursor)

executeQueries()