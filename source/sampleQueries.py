import pymysql, datetime, timedelta
import connect

def select_from_customers(cursor):
    print("Customers table:")
    cursor.execute("SELECT * FROM Customers")
    for x in cursor:
        print(x)

def select_from_staffs(cursor):
    print("Staffs table:")
    cursor.execute("SELECT * FROM Staffs")
    for x in cursor:
        print(x)

def select_from_cars(cursor):
    print("Cars table:")
    cursor.execute("SELECT * FROM Cars")
    for x in cursor:
        print(x)

def select_from_bookings(cursor):
    print("Bookings table:")
    cursor.execute("SELECT * FROM Bookings")
    for x in cursor:
        print(x)

def select_from_backlogs(cursor):
    print("Backlogs table:")
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
    connection = connect.connect_to_database()
    cursor = connection.cursor()

    #Retrieve all data
    select_from_customers(cursor)
    select_from_staffs(cursor)
    select_from_cars(cursor)
    select_from_bookings(cursor)
    select_from_backlogs(cursor)
    #Additional queries (for drawing graphs)
    select_number_of_bookings_per_day(cursor)
    select_number_of_returns_per_day(cursor)
    select_number_of_cars_of_the_same_type(cursor)
    select_profit_per_day(cursor)

    #Close connection
    cursor.close()
    connection.close()

execute_queries()