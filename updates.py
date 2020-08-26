import pymysql, datetime, timedelta
import connect

def update_customers_table(cursor, updated_values):
    sql = """UPDATE Customers
             SET Username = %s, Password = %s, FirstName = %s, LastName = %s, Email = %s
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
             SET EngineerID = %s, SignedID = %s, CarID = %s, Date = %s, Status = %s, Description = %s
             WHERE ID = %s"""
    cursor.execute(sql, updated_values)
    cursor.connection.commit()

def update_all():
    #Updated values
    updated_customer = ("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh123@gmail.com", 3)
    updated_staff = ("Minh34", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer", 3)
    updated_car = (None, "Toyota", "Sedan", "600 Nguyen Van Linh", "Available", "White", 4, 2, 6)
    updated_booking = (1, 10, "2020-8-23 14:30:00", "2020-8-27 15:30:00", 192, 5)
    updated_backlog = (2, 2, "7", "2020-8-23 11:15:00", "Done", "Change the oil", 3)

    #Connect to database
    connection = connect.connect_to_database()
    cursor = connection.cursor()

    #Update data
    update_customers_table(cursor, updated_customer)
    update_staffs_table(cursor, updated_staff)
    update_cars_table(cursor, updated_car)
    update_bookings_table(cursor, updated_booking)
    update_backlogs_table(cursor, updated_backlog)

    #Close connection
    cursor.close()
    connection.close()
    print("Done")

update_all()
