import pymysql, datetime, timedelta
import connect

def addSampleCustomers(cursor):
    sql = "INSERT INTO Customer (Username, Password, FirstName, LastName, Email) VALUES (%s, %s, %s, %s, %s)"
    customer1 = ("Tam", "12345678", "Tam", "Nguyen", "tam@gmail.com")
    customer2 = ("Nguyen", "23456781", "Nguyen", "Thanh", "nguyen123@gmail.com")
    customer3 = ("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh456@gmail.com")
    cursor.execute(sql, customer1)
    cursor.execute(sql, customer2)
    cursor.execute(sql, customer3)
    cursor.connection.commit()

def addSampleStaffs(cursor):
    sql = "INSERT INTO Staff (Username, Password, FirstName, LastName, Email, UserType) VALUES (%s, %s, %s, %s, %s, %s)"
    admin = ("Cuong_Nguyen", "11111111abcd", "Cuong", "Nguyen", "cuong@gmail.com", "Admin")
    manager = ("Tien_Nguyen", "abcd22222222", "Tien", "Nguyen", "tien222@gmail.com", "Manager")
    engineer1 = ("Minh33", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer")
    engineer2 = ("Tom", "abcdefgh", "Tom", "Nguyen", "tom@gmail.com", "Engineer")
    cursor.execute(sql, admin)
    cursor.execute(sql, manager)
    cursor.execute(sql, engineer1)
    cursor.execute(sql, engineer2)
    cursor.connection.commit()

def addSampleCars(cursor):
    sql = "INSERT INTO Car (MacAddress, Brand, Type, Location, Status, Color, Seat, Cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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
    cursor.execute(sql, car1)
    cursor.execute(sql, car2)
    cursor.execute(sql, car3)
    cursor.execute(sql, car4)
    cursor.execute(sql, car5)
    cursor.execute(sql, car6)
    cursor.execute(sql, car7)
    cursor.execute(sql, car8)
    cursor.execute(sql, car9)
    cursor.execute(sql, car10)
    cursor.connection.commit()

def addSampleBooking(cursor):
    sql = "INSERT INTO Booking (CustomerID, CarID, RentTime, ReturnTime, TotalCost) VALUES (%s, %s, %s, %s, %s)"
    booking1 = (1, 1, "2020-8-22 10:00:00", "2020-8-24 10:00:00", 96)
    booking2 = (3, 5, "2020-8-23 09:00:00", "2020-8-27 09:00:00", 384)
    cursor.execute(sql, booking1)
    cursor.execute(sql, booking2)
    cursor.connection.commit()

def addSampleBacklog(cursor):
    sql = "INSERT INTO Backlog (EngineerID, SignedID, CarID, Date, Status, Description) VALUES (%s, %s, %s, %s, %s, %s)"
    backlog1 = (1, 1, "3", "2020-8-21 10:30:00", "Done", "Car ran out of fuel")
    backlog2 = (1, 2, "4", "2020-8-22 15:45:00", "Done", "Replace the windshield")
    backlog3 = (2, None, "7", "2020-8-23 11:15:00", "Not done", "Change the oil")
    cursor.execute(sql, backlog1)
    cursor.execute(sql, backlog2)
    cursor.execute(sql, backlog3)
    cursor.connection.commit()

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

def addSampleData():
    #Connect to the database
    cursor = connect.connectToDatabase().cursor()
    #Add sample data to tables
    addSampleCustomers(cursor)
    addSampleStaffs(cursor)
    addSampleCars(cursor)
    addSampleBooking(cursor)
    addSampleBacklog(cursor)
    print("Data successfully added")
    #Retrieve all data
    selectFromCustomer(cursor)
    selectFromStaff(cursor)
    selectFromCar(cursor)
    selectFromBooking(cursor)
    selectFromBacklog(cursor)

addSampleData()