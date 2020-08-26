import pymysql, datetime, timedelta
import connect

def select_from_customer(cursor):
    print("Customer table:")
    cursor.execute("SELECT * FROM Customers")
    for x in cursor:
        print(x)

def select_from_staff(cursor):
    print("Staff table:")
    cursor.execute("SELECT * FROM Staffs")
    for x in cursor:
        print(x)

def select_from_car(cursor):
    print("Car table:")
    cursor.execute("SELECT * FROM Cars")
    for x in cursor:
        print(x)

def select_from_booking(cursor):
    print("Booking table:")
    cursor.execute("SELECT * FROM Bookings")
    for x in cursor:
        print(x)

def select_from_backlog(cursor):
    print("Backlog table:")
    cursor.execute("SELECT * FROM Backlogs")
    for x in cursor:
        print(x)

def select_number_of_bookings_per_day(cursor):
    print("Number of bookings per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, COUNT(DATE(RentTime)) AS Daily_Bookings FROM Bookings GROUP BY DATE(RentTime)")
    for x in cursor:
        print(x)

def select_number_of_returns_per_day(cursor):
    print("Number of returns per day:")
    cursor.execute("SELECT DATE(ReturnTime) AS Date, COUNT(DATE(ReturnTime)) AS Daily_Returns FROM Bookings GROUP BY DATE(ReturnTime)")
    for x in cursor:
        print(x)

def select_profit_per_day(cursor):
    print("Profit per day:")
    cursor.execute("SELECT DATE(RentTime) AS Date, SUM(TotalCost) AS Daily_Profit FROM Bookings GROUP BY DATE(RentTime)")
    for x in cursor:
        print(x)

def select_number_of_cars_of_the_same_type(cursor):
    print("Different types of cars:")
    cursor.execute("""
        SELECT Cars.Type, COUNT(Cars.Type) AS Number_Of_Cars
        FROM Bookings
        INNER JOIN Cars ON Bookings.CarID = Cars.ID
        GROUP BY Cars.Type"""
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