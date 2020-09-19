from database import Database
from passlib import hash

def add_sample_location(location):
    Database.insert_record_parameterized(
        "Locations(Latitude, Longitude, Address)",
        "(%s, %s, %s)",
        location
    )

def add_sample_customer(customer):
    Database.insert_record_parameterized(
        "Customers(Username, Password, FirstName, LastName, Email, Phone)",
        "(%s, %s, %s, %s, %s, %s)",
        customer
    )

def add_sample_staff(staff):
    Database.insert_record_parameterized(
        "Staffs(Username, Password, FirstName, LastName, Email, Phone, UserType, EngineerMacAddress)",
        "(%s, %s, %s, %s, %s, %s, %s, %s)",
        staff
    )

def add_sample_car(car):
    Database.insert_record_parameterized(
        "Cars(MacAddress, Brand, Type, LocationID, Status, Color, Seat, Cost)",
        "(%s, %s, %s, %s, %s, %s, %s, %s)",
        car
    )

def add_sample_booking(booking):
    Database.insert_record_parameterized(
        "Bookings(CustomerID, CarID, RentTime, ReturnTime, TotalCost, Status, EventID)",
        "(%s, %s, %s, %s, %s, %s, %s)",
        booking
    )

def add_sample_backlog(backlog):
    Database.insert_record_parameterized(
        "Backlogs(AssignedEngineerID, CarID, CreatedDate, Status, Description)",
        "(%s, %s, %s, %s, %s)",
        backlog
    )

def create_sample_staffs_data():
    #Staffs
    global staffs 
    staffs = []
    staffs.append(("cuong_nguyen", hash.sha256_crypt.hash("1!aA2222"), "Cuong", "Nguyen", "quoccuong242000@gmail.com","123456", "Engineer", "DC:F7:56:2D:C1:97"))
    staffs.append(("minh_nguyen", hash.sha256_crypt.hash("2@aA3333"), "Minh", "Nguyen", "minh456@gmail.com", "123456789", "Admin", ""))
    staffs.append(("tam_nguyen", hash.sha256_crypt.hash("3#aA4444"), "Tam", "Nguyen", "tom@gmail.com", "12345678970", "Manager", ""))

def create_sample_customers_data():
    #Customers
    global customers 
    customers = []
    customers.append(("tamnguyen", hash.sha256_crypt.hash("1!aA1111"), "Tam", "Nguyen", "tam@gmail.com", "123456"))
    customers.append(("tiennguyen", hash.sha256_crypt.hash("2@aA2222"), "Tien", "Nguyen", "tien@gmail.com", "12343456"))
    customers.append(("minhnguyen", hash.sha256_crypt.hash("3#aA3333"), "Minh", "Nguyen", "minh@gmail.com", "12345678"))
   
def create_sample_locations_data():
    #Customers
    global locations
    locations = []
    locations.append(("10.729792", "106.692107", "RMIT Vietnam, 702 Nguyễn Văn Linh, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Vietnam"))
    locations.append(("10.728943" , "106.718845", "Crescent Mall, 101 Tôn Dật Tiên, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Vietnam"))

def create_sample_cars_data():
    #Cars
    global cars 
    cars = []
    cars.append(("DC:A6:32:4A:0C:41", "Ford", "Sedan", 1, "Unavailable", "White", 4, 2))
    cars.append(("", "BMW", "Minivan", 1, "Available", "Blue", 2, 3))
    cars.append(("", "Audi", "Sedan", 2, "Available", "Black", 4, 2))
    cars.append(("", "Toyota", "Truck", 1, "Available", "Blue", 2, 4))
    cars.append(("", "Ford", "Truck", 2, "Unavailable", "Yellow", 2, 4))
    cars.append(("", "Toyota", "Sedan", 2, "Available", "White", 4, 2))
    cars.append(("", "BMW", "Truck", 2, "Available", "Black", 2, 4))
    cars.append(("", "Audi", "Minivan", 2, "Available", "Blue", 2, 3))
    cars.append(("", "Ford", "Minivan", 2, "Available", "White", 2, 3))
    cars.append(("", "BMW", "Sedan", 1, "Available", "Yellow", 4, 2))
    cars.append(("", "Ford", "Truck", 1, "Available", "Red", 4, 5))
    cars.append(("", "Toyota", "Sedan", 1, "Available", "Grey", 4, 4))
    cars.append(("", "BMW", "Truck", 2, "Available", "White", 4, 7))
    cars.append(("", "Audi", "Minivan", 1, "Available", "Red", 5, 7))
    cars.append(("", "Ford", "Minivan", 2, "Available", "Blue", 4, 6))
    cars.append(("", "Ford", "Truck", 1, "Available", "White", 2, 4))
    cars.append(("", "Toyota", "Sedan", 1, "Available", "Red", 4, 5))
    cars.append(("", "BMW", "Truck", 1, "Available", "Red", 2, 4))
    cars.append(("", "Audi", "Minivan", 2, "Available", "White", 4, 5))
    cars.append(("", "Ford", "Minivan", 2, "Available", "Red", 4, 5))
    
def create_sample_bookings_data():
    #Bookings
    global bookings 
    bookings = []
    bookings.append((1, 1, "2020-8-21 10:00:00", "2020-8-24 10:00:00", 144, "Booked", ""))
    bookings.append((3, 5, "2020-8-22 09:00:00", "2020-8-27 09:00:00", 480, "Booked", ""))
    bookings.append((2, 2, "2020-8-22 09:30:00", "2020-8-26 09:30:00", 288, "Cancelled", ""))
    bookings.append((3, 6, "2020-8-23 15:45:00", "2020-8-28 15:45:00", 240, "Cancelled", ""))
    bookings.append((1, 10, "2020-8-23 14:30:00", "2020-8-27 14:30:00", 192, "Booked", ""))
    bookings.append((2, 8, "2020-8-23 12:00:00", "2020-8-30 12:00:00", 504, "Booked", ""))
    bookings.append((1, 5, "2020-8-24 11:15:00", "2020-8-25 11:15:00", 96, "Booked", ""))
    bookings.append((1, 1, "2020-09-01 10:00:00", "2020-09-02 10:00:00", 200, "Booked", ""))
    bookings.append((2, 8, "2020-09-01 10:00:00", "2020-09-02 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 11, "2020-09-01 10:00:00", "2020-09-03 10:00:00", 200, "Booked", ""))
    bookings.append((1, 15, "2020-09-01 10:00:00", "2020-09-04 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 13, "2020-09-01 10:00:00", "2020-09-05 10:00:00", 1500, "Booked", ""))
    bookings.append((2, 19, "2020-09-01 10:00:00", "2020-09-05 10:00:00", 200, "Booked", ""))
    bookings.append((2, 16, "2020-09-05 10:00:00", "2020-09-07 10:00:00", 200, "Booked", ""))
    bookings.append((1, 20, "2020-09-05 10:00:00", "2020-09-07 10:00:00", 500, "Booked", ""))
    bookings.append((1, 16, "2020-09-06 10:00:00", "2020-09-07 10:00:00", 200, "Booked", ""))
    bookings.append((3, 20, "2020-09-07 10:00:00", "2020-09-08 10:00:00", 200, "Booked", ""))
    bookings.append((2, 17, "2020-09-07 10:00:00", "2020-09-09 10:00:00", 700, "Booked", ""))
    bookings.append((3, 11, "2020-09-07 10:00:00", "2020-09-09 10:00:00", 900, "Booked", ""))
    bookings.append((2, 13, "2020-09-08 10:00:00", "2020-09-09 10:00:00", 103, "Booked", ""))
    bookings.append((1, 2, "2020-09-08 10:00:00", "2020-09-09 10:00:00", 1500, "Booked", ""))
    bookings.append((1, 2, "2020-09-08 10:00:00", "2020-09-09 10:00:00", 200, "Booked", ""))
    bookings.append((2, 3, "2020-09-09 10:00:00", "2020-09-10 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 6, "2020-09-10 10:00:00", "2020-09-12 10:00:00", 200, "Booked", ""))
    bookings.append((3, 2, "2020-09-11 10:00:00", "2020-09-12 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 9, "2020-09-11 10:00:00", "2020-09-12 10:00:00", 1500, "Booked", ""))
    bookings.append((2, 7, "2020-09-11 10:00:00", "2020-09-12 10:00:00", 200, "Booked", ""))
    bookings.append((2, 12, "2020-09-11 10:00:00", "2020-09-13 10:00:00", 200, "Booked", ""))
    bookings.append((1, 13, "2020-09-11 10:00:00", "2020-09-13 10:00:00", 500, "Booked", ""))
    bookings.append((3, 11, "2020-09-11 10:00:00", "2020-09-13 10:00:00", 200, "Booked", ""))
    bookings.append((3, 15, "2020-09-11 10:00:00", "2020-09-13 10:00:00", 200, "Booked", ""))
    bookings.append((2, 13, "2020-09-12 10:00:00", "2020-09-15 10:00:00", 700, "Cancelled", ""))
    bookings.append((3, 19, "2020-09-12 10:00:00", "2020-09-15 10:00:00", 900, "Booked", ""))
    bookings.append((2, 16, "2020-09-12 10:00:00", "2020-09-15 10:00:00", 103, "Booked", ""))
    bookings.append((1, 20, "2020-09-12 10:00:00", "2020-09-15 10:00:00", 1500, "Booked", ""))
    bookings.append((1, 16, "2020-09-12 10:00:00", "2020-09-15 10:00:00", 200, "Booked", ""))
    bookings.append((2, 20, "2020-09-13 10:00:00", "2020-09-15 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 17, "2020-09-13 10:00:00", "2020-09-15 10:00:00", 200, "Booked", ""))
    bookings.append((2, 11, "2020-09-13 10:00:00", "2020-09-15 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 13, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 1500, "Booked", ""))
    bookings.append((2, 12, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 200, "Booked", ""))
    bookings.append((2, 6, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 200, "Booked", ""))
    bookings.append((1, 14, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 500, "Booked", ""))
    bookings.append((2, 15, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 200, "Cancelled", ""))
    bookings.append((3, 14, "2020-09-13 10:00:00", "2020-09-14 10:00:00", 200, "Booked", ""))
    bookings.append((2, 4, "2020-09-13 10:00:00", "2020-09-16 10:00:00", 700, "Booked", ""))
    bookings.append((3, 9, "2020-09-13 10:00:00", "2020-09-16 10:00:00", 900, "Booked", ""))
    bookings.append((2, 7, "2020-09-14 10:00:00", "2020-09-16 10:00:00", 103, "Booked", ""))
    bookings.append((1, 2, "2020-09-14 10:00:00", "2020-09-16 10:00:00", 1500, "Booked", ""))
    bookings.append((1, 2, "2020-09-14 10:00:00", "2020-09-16 10:00:00", 200, "Booked", ""))
    bookings.append((2, 3, "2020-09-14 10:00:00", "2020-09-17 10:00:00", 1500, "Cancelled", ""))
    bookings.append((3, 6, "2020-09-15 10:00:00", "2020-09-17 10:00:00", 200, "Cancelled", ""))
    bookings.append((2, 2, "2020-09-15 10:00:00", "2020-09-17 10:00:00", 1500, "Booked", ""))
    bookings.append((3, 9, "2020-09-15 10:00:00", "2020-09-17 10:00:00", 1500, "Cancelled", ""))
    bookings.append((2, 7, "2020-09-15 10:00:00", "2020-09-17 10:00:00", 200, "Booked", ""))
    bookings.append((2, 12, "2020-09-15 10:00:00", "2020-09-18 10:00:00", 200, "Booked", ""))
    bookings.append((1, 13, "2020-09-15 10:00:00", "2020-09-18 10:00:00", 500, "Booked", ""))

def create_sample_backlogs_data():
    #Backlogs
    global backlogs 
    backlogs = []
    backlogs.append((1, "3", "2020-8-21 10:30:00", "Done", "Car ran out of fuel"))
    backlogs.append((1, "4", "2020-8-22 15:45:00", "Not done", "Replace the windshield"))
    backlogs.append((1, "7", "2020-8-23 11:15:00", "Not done", "Change the oil"))
   
def add_sample_data():
    create_sample_staffs_data()
    create_sample_customers_data()
    create_sample_cars_data()
    create_sample_backlogs_data()
    create_sample_bookings_data()
    create_sample_locations_data()
    
    for location in locations:
        add_sample_location(location)

    for car in cars:
        add_sample_car(car)

    for staff in staffs:
        add_sample_staff(staff)

    for customer in customers:
        add_sample_customer(customer)

    for booking in bookings:
        add_sample_booking(booking)

    for backlog in backlogs:
        add_sample_backlog(backlog)

    print("Data successfully added")

add_sample_data()