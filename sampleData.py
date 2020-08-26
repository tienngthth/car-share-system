import pymysql, datetime, timedelta
import connect

def add_sample_customer(cursor, customer):
    sql = "INSERT INTO Customers (Username, Password, FirstName, LastName, Email) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, customer)
    cursor.connection.commit()

def add_sample_staff(cursor, staff):
    sql = "INSERT INTO Staffs (Username, Password, FirstName, LastName, Email, UserType) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, staff)
    cursor.connection.commit()

def add_sample_car(cursor, car):
    sql = "INSERT INTO Cars (MacAddress, Brand, Type, Location, Status, Color, Seat, Cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, car)
    cursor.connection.commit()

def add_sample_booking(cursor, booking):
    sql = "INSERT INTO Bookings (CustomerID, CarID, RentTime, ReturnTime, TotalCost) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, booking)
    cursor.connection.commit()

def add_sample_backlog(cursor, backlog):
    sql = "INSERT INTO Backlogs (EngineerID, SignedID, CarID, Date, Status, Description) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, backlog)
    cursor.connection.commit()

def add_sample_data():
    #Customers
    customer1 = ("Tam", "12345678", "Tam", "Nguyen", "tam@gmail.com")
    customer2 = ("Nguyen", "23456781", "Nguyen", "Thanh", "nguyen123@gmail.com")
    customer3 = ("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh456@gmail.com")
    customer4 = ("Tommy", "2468abc1234", "Tommy", "Nguyen", "tommy24@gmail.com")
    #Staffs
    admin = ("Cuong_Nguyen", "11111111abcd", "Cuong", "Nguyen", "cuong@gmail.com", "Admin")
    manager = ("Tien_Nguyen", "abcd22222222", "Tien", "Nguyen", "tien222@gmail.com", "Manager")
    engineer1 = ("Minh33", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer")
    engineer2 = ("Tom", "abcdefgh", "Tom", "Nguyen", "tom@gmail.com", "Engineer")
    engineer3 = ("Tam2", "abcdefghijk", "Tam", "Thanh", "tamthanh@gmail.com", "Engineer")
    #Cars
    car1 = (None, "Ford", "Sedan", "28 Do Xuan Hop", "Unavailable", "White", 4, 2)
    car2 = (None, "BMW", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3)
    car3 = (None, "Audi", "Sedan", "702 Nguyen Van Linh", "Available", "Black", 4, 2)
    car4 = (None, "Toyota", "Truck", "702 Nguyen Van Linh", "Available", "Blue", 2, 4)
    car5 = (None, "Ford", "Truck", "65 Nguyen Huu Tho", "Unavailable", "Yellow", 2, 4)
    car6 = (None, "Toyota", "Sedan", "702 Nguyen Van Linh", "Available", "White", 4, 2)
    car7 = (None, "BMW", "Truck", "702 Nguyen Van Linh", "Available", "Black", 2, 4)
    car8 = (None, "Audi", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3)
    car9 = (None, "Ford", "Minivan", "702 Nguyen Van Linh", "Available", "White", 2, 3)
    car10 = (None, "BMW", "Sedan", "702 Nguyen Van Linh", "Available", "Yellow", 4, 2)
    #Bookings
    booking1 = (1, 1, "2020-8-21 10:00:00", "2020-8-24 10:00:00", 144)
    booking2 = (3, 5, "2020-8-22 09:00:00", "2020-8-27 09:00:00", 480)
    booking3 = (2, 2, "2020-8-22 09:30:00", "2020-8-26 09:30:00", 288)
    booking4 = (3, 6, "2020-8-23 15:45:00", "2020-8-28 15:45:00", 240)
    booking5 = (1, 10, "2020-8-23 14:30:00", "2020-8-27 14:30:00", 192)
    booking6 = (2, 8, "2020-8-23 12:00:00", "2020-8-30 12:00:00", 504)
    booking7 = (1, 5, "2020-8-24 11:15:00", "2020-8-25 11:15:00", 96)
    #Backlogs
    backlog1 = (1, 1, 3, "2020-8-21 10:30:00", "Done", "Car ran out of fuel")
    backlog2 = (1, 2, 4, "2020-8-22 15:45:00", "Done", "Replace the windshield")
    backlog3 = (2, None, 7, "2020-8-23 11:15:00", "Not done", "Change the oil")


    #Connect to the database
    connection = connect.connect_to_database()
    cursor = connection.cursor()

    #Add customers to table
    add_sample_customer(cursor, customer1)
    add_sample_customer(cursor, customer2)
    add_sample_customer(cursor, customer3)
    add_sample_customer(cursor, customer4)
    #Add staffs to table
    add_sample_staff(cursor, admin)
    add_sample_staff(cursor, manager)
    add_sample_staff(cursor, engineer1)
    add_sample_staff(cursor, engineer2)
    add_sample_staff(cursor, engineer3)
    #Add cars to table
    add_sample_car(cursor, car1)
    add_sample_car(cursor, car2)
    add_sample_car(cursor, car3)
    add_sample_car(cursor, car4)
    add_sample_car(cursor, car5)
    add_sample_car(cursor, car6)
    add_sample_car(cursor, car7)
    add_sample_car(cursor, car8)
    add_sample_car(cursor, car9)
    add_sample_car(cursor, car10)
    #Add bookings to table
    add_sample_booking(cursor, booking1)
    add_sample_booking(cursor, booking2)
    add_sample_booking(cursor, booking3)
    add_sample_booking(cursor, booking4)
    add_sample_booking(cursor, booking5)
    add_sample_booking(cursor, booking6)
    add_sample_booking(cursor, booking7)
    #Add backlogs to table
    add_sample_backlog(cursor, backlog1)
    add_sample_backlog(cursor, backlog2)
    add_sample_backlog(cursor, backlog3)

    #Close connection
    cursor.close()
    connection.close()
    print("Data successfully added")

add_sample_data()