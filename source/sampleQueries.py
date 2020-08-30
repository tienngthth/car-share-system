import pymysql
from model.database import Database

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

def update_customers_table(cursor, updated_values):
    sql = """UPDATE Customers
             SET Username = %s, Password = %s, FirstName = %s, LastName = %s, Email = %s, Phone = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def update_staffs_table(cursor, updated_values):
    sql = """UPDATE Staffs
             SET Username = %s, Password = %s, FirstName = %s, LastName = %s, Email = %s, UserType = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def update_cars_table(cursor, updated_values):
    sql = """UPDATE Cars
             SET MacAddress = %s, Brand = %s, Type = %s, Location = %s, Status = %s, Color = %s, Seat = %s, Cost = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def update_bookings_table(cursor, updated_values):
    sql = """UPDATE Bookings
             SET CustomerID = %s, CarID = %s, RentTime = %s, ReturnTime = %s, TotalCost = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def update_backlogs_table(cursor, updated_values):
    sql = """UPDATE Backlogs
             SET AssignedEngineerID = %s, SignedEngineerID = %s, CarID = %s, Date = %s, Status = %s, Description = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def delete_customer(cursor, ID):
    sql = """DELETE FROM Customers
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_staff(cursor, ID):
    sql = """DELETE FROM Staffs
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_car(cursor, ID):
    sql = """DELETE FROM Cars
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_booking(cursor, ID):
    sql = """DELETE FROM Bookings
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_backlog(cursor, ID):
    sql = """DELETE FROM Backlogs
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()


def execute_queries():
    #Connect to the database
    Database.setup_connection()
    cursor = Database.curs

    # #Retrieve all data
    # select_from_customers(cursor)
    # select_from_staffs(cursor)
    # select_from_cars(cursor)
    # select_from_bookings(cursor)    
    select_from_backlogs(cursor)
    # #Additional queries (for drawing graphs)
    # select_number_of_bookings_per_day(cursor)
    # select_number_of_returns_per_day(cursor)
    # select_number_of_cars_of_the_same_type(cursor)
    # select_profit_per_day(cursor)

    # #Updated values
    # updated_customer = ("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh123@gmail.com", "13572486901", 3)
    # updated_staff = ("Minh34", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer", 3)
    # updated_car = (None, "Toyota", "Sedan", "600 Nguyen Van Linh", "Available", "White", 4, 2, 6)
    # updated_booking = (1, 10, "2020-8-23 14:30:00", "2020-8-27 15:30:00", 192, 5)
    # updated_backlog = (2, 2, "7", "2020-8-23 11:15:00", "Done", "Change the oil", 3)

    # #Update data
    # update_customers_table(cursor, updated_customer)
    # update_staffs_table(cursor, updated_staff)
    # update_cars_table(cursor, updated_car)
    # update_bookings_table(cursor, updated_booking)
    # update_backlogs_table(cursor, updated_backlog)

    # #Retrieve all data
    # select_from_customers(cursor)
    # select_from_staffs(cursor)
    # select_from_cars(cursor)
    # select_from_bookings(cursor)
    # select_from_backlogs(cursor)

    # #Delete data
    # delete_customer(cursor, 4)
    # delete_staff(cursor, 5)
    # delete_car(cursor, 9)
    # delete_booking(cursor, 7)
    # delete_backlog(cursor, 3)

    # #Retrieve all data
    # select_from_customers(cursor)
    # select_from_staffs(cursor)
    # select_from_cars(cursor)
    # select_from_bookings(cursor)
    # select_from_backlogs(cursor)

    #Close connection
    cursor.close()
    
execute_queries()
