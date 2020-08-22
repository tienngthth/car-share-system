import pymysql
import connect

def addSampleCustomers(cursor):
    sql = "INSERT INTO Customer (ID, Username, Password, FirstName, LastName, Email) VALUES (%s, %s, %s, %s, %s, %s)"
    customer1 = ("1", "Tam", "12345678", "Tam", "Nguyen", "tam@gmail.com")
    customer2 = ("2", "Nguyen", "23456781", "Nguyen", "Thanh", "nguyen123@gmail.com")
    customer3 = ("3", "Thanh", "13572468abc", "Thanh", "Nguyen", "thanh456@gmail.com")
    cursor.execute(sql, customer1)
    cursor.execute(sql, customer2)
    cursor.execute(sql, customer3)

def addSampleStaffs(cursor):
    sql = "INSERT INTO Staff (ID, Username, Password, FirstName, LastName, Email, UserType) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    admin = ("1", "Cuong_Nguyen", "11111111abcd", "Cuong", "Nguyen", "cuong@gmail.com", "Admin")
    manager = ("2", "Tien_Nguyen", "abcd22222222", "Tien", "Nguyen", "tien222@gmail.com", "Manager")
    staff = ("3", "Minh33", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer")
    cursor.execute(sql, admin)
    cursor.execute(sql, manager)
    cursor.execute(sql, staff)

def addSampleCars(cursor):
    sql = "INSERT INTO Car (ID, Brand, Type, Location, Status, Color, Seat, Cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    car1 = ("1", "Ford", "Sedan", "28 Do Xuan Hop", "Unavailable", "White", 4, 2)
    car2 = ("2", "BMW", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3)
    car3 = ("3", "Audi", "Sedan", "702 Nguyen Van Linh", "Available", "Black", 4, 2)
    car4 = ("4", "Toyota", "Truck", "702 Nguyen Van Linh", "Available", "Blue", 2, 4)
    car5 = ("5", "Ford", "Truck", "65 Nguyen Huu Tho", "Unavailable", "Yellow", 2, 4)
    car6 = ("6", "Toyota", "Sedan", "702 Nguyen Van Linh", "Available", "White", 4, 2)
    car7 = ("7", "BMW", "Truck", "702 Nguyen Van Linh", "Available", "Black", 2, 4)
    car8 = ("8", "Audi", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3)
    car9 = ("9", "Ford", "Minivan", "702 Nguyen Van Linh", "Available", "White", 2, 3)
    car10 = ("10", "BMW", "Sedan", "702 Nguyen Van Linh", "Available", "Yellow", 4, 2)
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

def addSampleBooking(cursor):
    sql = "INSERT INTO Booking (ID, CustomerID, CarID, RentTime, ReturnTime, TotalCost) VALUES (%s, %s, %s, %s, %s, %s)"
    booking1 = ("1", "1", "1", "2020-8-22 10:00:00", "2020-8-24 10:00:00", 96)
    booking2 = ("2", "3", "5", "2020-8-23 09:00:00", "2020-8-27 09:00:00", 384)
    cursor.execute(sql, booking1)
    cursor.execute(sql, booking2)

def addSampleBacklog(cursor):
    sql = "INSERT INTO Backlog (ID, EngineerID, CarID, Date, Status, Description) VALUES (%s, %s, %s, %s, %s, %s)"
    backlog1 = ("1", "1", "3", "2020-8-21 10:30:00", "Done", "Car ran out of fuel")
    backlog2 = ("2", "1", "4", "2020-8-22 15:45:00", "Not done", "Replace the windshield")
    cursor.execute(sql, backlog1)
    cursor.execute(sql, backlog2)

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