import pymysql, datetime, timedelta
import connect

def select_from_customer(cursor):
    print("Customer table:")
    cursor.execute("SELECT * FROM Customer")
    for x in cursor:
        print(x)

def select_from_staff(cursor):
    print("Staff table:")
    cursor.execute("SELECT * FROM Staff")
    for x in cursor:
        print(x)

def select_from_car(cursor):
    print("Car table:")
    cursor.execute("SELECT * FROM Car")
    for x in cursor:
        print(x)

def select_from_booking(cursor):
    print("Booking table:")
    cursor.execute("SELECT * FROM Booking")
    for x in cursor:
        print(x)

def select_from_backlog(cursor):
    print("Backlog table:")
    cursor.execute("SELECT * FROM Backlog")
    for x in cursor:
        print(x)

def select_number_of_bookings_per_day(cursor):
    print("Number of bookings per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, COUNT(DATE(RentTime)) AS Daily_Bookings FROM Booking GROUP BY DATE(RentTime)")
    for x in cursor:
        print(x)

def select_number_of_returns_per_day(cursor):
    print("Number of returns per day:")
    cursor.execute("SELECT DATE(ReturnTime) AS Date, COUNT(DATE(ReturnTime)) AS Daily_Returns FROM Booking GROUP BY DATE(ReturnTime)")
    for x in cursor:
        print(x)

def select_profit_per_day(cursor):
    print("Profit per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, SUM(TotalCost) AS Daily_Profit FROM Booking GROUP BY DATE(RentTime)")
    for x in cursor:
        print(x)

def select_number_of_cars_of_the_same_type(cursor):
    print("Different types of cars:")
    cursor.execute("""
        SELECT Car.Type, COUNT(Car.Type) AS Number_Of_Cars
        FROM Booking
        INNER JOIN Car ON Booking.CarID = Car.ID
        GROUP BY Car.Type"""
    )
    for x in cursor:
        print(x)

def execute_queries():
    #Connect to the database
    cursor = connect.connect_to_database().cursor()
    #Retrieve all data
    select_from_customer(cursor)
    select_from_staff(cursor)
    select_from_car(cursor)
    select_from_booking(cursor)
    select_from_backlog(cursor)
    #Additional queries (for drawing graphs)
    select_number_of_bookings_per_day(cursor)
    select_number_of_returns_per_day(cursor)
    select_number_of_cars_of_the_same_type(cursor)
    select_profit_per_day(cursor)
    cursor.close()

execute_queries()