from model.database import Database

def add_sample_customer(customer):
    Database.insert_record(
        "Customer(Username, Password, FirstName, LastName, Email)",
        "(%s, %s, %s, %s, %s)",
        customer
    )

def add_sample_staff(staff):
    Database.insert_record(
        "Staff (Username, Password, FirstName, LastName, Email, UserType)",
        "(%s, %s, %s, %s, %s, %s)",
        staff
    )

def add_sample_car(car):
    Database.insert_record(
        "Car(MacAddress, Brand, Type, Location, Status, Color, Seat, Cost)",
        "(%s, %s, %s, %s, %s, %s, %s, %s)",
        car
    )

def add_sample_booking(booking):
    Database.insert_record(
        "Booking (CustomerID, CarID, RentTime, ReturnTime, TotalCost)",
        "(%s, %s, %s, %s, %s)",
        booking
    )

def add_sample_backlog(backlog):
    Database.insert_record(
        "Backlog (AssignedEngineerID, SignedEngineerID, CarID, Date, Status, Description)",
        "(%s, %s, %s, %s, %s, %s)",
        backlog
    )

def create_sample_staffs_data():
    #Staffs
    global staffs 
    staffs = []
    staffs.append(("Cuong_Nguyen", "11111111abcd", "Cuong", "Nguyen", "cuong@gmail.com", "Admin"))
    staffs.append(("Tien_Nguyen", "abcd22222222", "Tien", "Nguyen", "tien222@gmail.com", "Manager"))
    staffs.append(("Minh33", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "Engineer"))
    staffs.append(("Tom", "abcdefgh", "Tom", "Nguyen", "tom@gmail.com", "Engineer"))

def create_sample_cars_data():
    #Cars
    global cars 
    cars = []
    cars.append((None, "Ford", "Sedan", "28 Do Xuan Hop", "Unavailable", "White", 4, 2))
    cars.append((None, "BMW", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3))
    cars.append((None, "Audi", "Sedan", "702 Nguyen Van Linh", "Available", "Black", 4, 2))
    cars.append((None, "Toyota", "Truck", "702 Nguyen Van Linh", "Available", "Blue", 2, 4))
    cars.append((None, "Ford", "Truck", "65 Nguyen Huu Tho", "Unavailable", "Yellow", 2, 4))
    cars.append((None, "Toyota", "Sedan", "702 Nguyen Van Linh", "Available", "White", 4, 2))
    cars.append((None, "BMW", "Truck", "702 Nguyen Van Linh", "Available", "Black", 2, 4))
    cars.append((None, "Audi", "Minivan", "702 Nguyen Van Linh", "Available", "Blue", 2, 3))
    cars.append((None, "Ford", "Minivan", "702 Nguyen Van Linh", "Available", "White", 2, 3))
    cars.append((None, "BMW", "Sedan", "702 Nguyen Van Linh", "Available", "Yellow", 4, 2))
   
def create_sample_bookings_data():
    #Bookings
    global bookings 
    bookings = []
    bookings.append((1, 1, "2020-8-21 10:00:00", "2020-8-24 10:00:00", 144))
    bookings.append((3, 5, "2020-8-22 09:00:00", "2020-8-27 09:00:00", 480))
    bookings.append((2, 2, "2020-8-22 09:30:00", "2020-8-26 09:30:00", 288))
    bookings.append((3, 6, "2020-8-23 15:45:00", "2020-8-28 15:45:00", 240))
    bookings.append((1, 10, "2020-8-23 14:30:00", "2020-8-27 14:30:00", 192))
    bookings.append((2, 8, "2020-8-23 12:00:00", "2020-8-30 12:00:00", 504))
    bookings.append((1, 5, "2020-8-24 11:15:00", "2020-8-25 11:15:00", 96))

def create_sample_backlogs_data():
    #Backlogs
    global backlogs 
    backlogs = []
    backlogs.append((1, 1, "3", "2020-8-21 10:30:00", "Done", "Car ran out of fuel"))
    backlogs.append((1, 2, "4", "2020-8-22 15:45:00", "Done", "Replace the windshield"))
    backlogs.append((2, None, "7", "2020-8-23 11:15:00", "Not done", "Change the oil"))
   
def create_sample_customers_data():
    #Customers
    global customers 
    customers = []
    customers.append(("Tam", "12345678", "Tam", "Nguyen", "tam@gmail.com"))
    customers.append(("Nguyen", "23456781", "Nguyen", "Thanh", "nguyen123@gmail.com"))
    customers.append(("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh456@gmail.com"))

def add_sample_data():
    create_sample_staffs_data()
    create_sample_customers_data()
    create_sample_cars_data()
    create_sample_backlogs_data()
    create_sample_bookings_data()
    
    for car in cars:
        add_sample_car(car)

    for customer in customers:
        add_sample_customer(customer)

    for booking in bookings:
        add_sample_booking(booking)

    for staff in staffs:
        add_sample_staff(staff)

    for backlog in backlogs:
        add_sample_backlog(backlog)
        
    print("Data successfully added")

