from model.database import Database

def add_sample_customer(customer):
    Database.insert_record_parameterized(
        "Customers(Username, Password, FirstName, LastName, Email, Phone)",
        "(%s, %s, %s, %s, %s, %s)",
        customer
    )

def add_sample_staff(staff):
    Database.insert_record_parameterized(
        "Staffs(Username, Password, FirstName, LastName, Email, Phone, UserType)",
        "(%s, %s, %s, %s, %s, %s, %s)",
        staff
    )

def add_sample_car(car):
    Database.insert_record_parameterized(
        "Cars(MacAddress, Brand, Type, Latitude, Longtitude, Status, Color, Seat, Cost)",
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        car
    )

def add_sample_booking(booking):
    Database.insert_record_parameterized(
        "Bookings(CustomerID, CarID, RentTime, ReturnTime, TotalCost, Status)",
        "(%s, %s, %s, %s, %s, %s)",
        booking
    )

def add_sample_backlog(backlog):
    Database.insert_record_parameterized(
        "Backlogs(AssignedEngineerID, SignedEngineerID, CarID, Date, Status, Description)",
        "(%s, %s, %s, %s, %s, %s)",
        backlog
    )

def create_sample_staffs_data():
    #Staffs
    global staffs 
    staffs = []
    staffs.append(("Cuong_Nguyen", "11111111abcd", "Cuong", "Nguyen", "cuong@gmail.com","123456", "Admin"))
    staffs.append(("Tien_Nguyen", "abcd22222222", "Tien", "Nguyen", "tien222@gmail.com", "1234567", "Manager"))
    staffs.append(("Minh33", "ab33333333cd", "Minh", "Nguyen", "minh456@gmail.com", "123456789", "Engineer"))
    staffs.append(("Tom", "abcdefgh", "Tom", "Nguyen", "tom@gmail.com", "12345678970", "Engineer"))

def create_sample_cars_data():
    #Cars
    global cars 
    cars = []
    cars.append(("DC:A6:32:4A:0C:41", "Ford", "Sedan", 10.729683, 106.693183, "Unavailable", "White", 4, 2))
    cars.append(("", "BMW", "Minivan", 10.729683, 106.693183, "Available", "Blue", 2, 3))
    cars.append(("", "Audi", "Sedan", 10.729683, 106.693183, "Available", "Black", 4, 2))
    cars.append(("", "Toyota", "Truck", 10.729683, 106.693183, "Available", "Blue", 2, 4))
    cars.append(("", "Ford", "Truck", 10.729683, 106.693183, "Unavailable", "Yellow", 2, 4))
    cars.append(("", "Toyota", "Sedan", 10.729683, 106.693183, "Available", "White", 4, 2))
    cars.append(("", "BMW", "Truck", 10.729683, 106.693183, "Available", "Black", 2, 4))
    cars.append(("", "Audi", "Minivan", 10.729683, 106.693183, "Available", "Blue", 2, 3))
    cars.append(("", "Ford", "Minivan", 10.729683, 106.693183, "Available", "White", 2, 3))
    cars.append(("", "BMW", "Sedan", 10.729683, 106.693183, "Available", "Yellow", 4, 2))
   
def create_sample_bookings_data():
    #Bookings
    global bookings 
    bookings = []
    bookings.append((1, 1, "2020-8-21 10:00:00", "2020-8-24 10:00:00", 144, "Booked"))
    bookings.append((3, 5, "2020-8-22 09:00:00", "2020-8-27 09:00:00", 480, "Booked"))
    bookings.append((2, 2, "2020-8-22 09:30:00", "2020-8-26 09:30:00", 288, "Cancelled"))
    bookings.append((3, 6, "2020-8-23 15:45:00", "2020-8-28 15:45:00", 240, "Cancelled"))
    bookings.append((1, 10, "2020-8-23 14:30:00", "2020-8-27 14:30:00", 192, "Booked"))
    bookings.append((2, 8, "2020-8-23 12:00:00", "2020-8-30 12:00:00", 504, "Booked"))
    bookings.append((1, 5, "2020-8-24 11:15:00", "2020-8-25 11:15:00", 96, "Booked"))

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
    customers.append(("Tam", "12345678", "Tam", "Nguyen", "tam@gmail.com", "123456"))
    customers.append(("Nguyen", "23456781", "Nguyen", "Thanh", "nguyen123@gmail.com", "12343456"))
    customers.append(("Thanh", "13572468abc", "Thanh", "Nguyen", "thanh456@gmail.com", "12345678"))

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

