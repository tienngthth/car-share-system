from model.database import Database

def create_customer_table():
    Database.create_table(
        "Customers", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(256), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            Phone VARCHAR(20),
            PRIMARY KEY(ID)
        ) """
    )
                
def create_staff_table():
    Database.create_table(
        "Staffs", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(256), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            Phone VARCHAR(20),
            UserType VARCHAR(10),
            EngineerMACAddress VARCHAR(50),
            PRIMARY KEY(ID)
        ) """
    )

def create_car_table():
    Database.create_table(
        "Cars", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            MacAddress VARCHAR(50),
            Brand VARCHAR(20),
            Type VARCHAR(20),
            LocationID INT,  
            Status VARCHAR(20),
            Color VARCHAR(20),
            Seat INT,
            Cost INT,
            PRIMARY KEY(ID),
            FOREIGN KEY (LocationID) REFERENCES Locations(ID)
        ) """
    )

def create_location_table():
    Database.create_table(
        "Locations",
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            Latitude DOUBLE,
            Longitude DOUBLE,
            Address VARCHAR(50),
            PRIMARY KEY (ID)
        )"""
    )

def create_booking_table():
    Database.create_table(
        "Bookings", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            CustomerID INT,
            CarID INT,
            RentTime DATETIME, 
            ReturnTime DATETIME, 
            TotalCost INT,
            Status VARCHAR(20),
            PRIMARY KEY(ID),
            FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
            FOREIGN KEY (CarID) REFERENCES Cars(ID)
        ) """
    )

def create_backlog_table():
    Database.create_table(
        "Backlogs", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            AssignedEngineerID INT,
            SignedEngineerID INT,
            CarID INT,
            Date DATETIME, 
            Status VARCHAR(20),
            Description VARCHAR(100),
            PRIMARY KEY(ID),
            FOREIGN KEY (AssignedEngineerID) REFERENCES Staffs(ID),
            FOREIGN KEY (SignedEngineerID) REFERENCES Staffs(ID),
            FOREIGN KEY (CarID) REFERENCES Cars(ID)
        ) """
    )

def create_all_tables():
    Database.execute_command("DROP TABLE IF EXISTS Bookings")
    Database.execute_command("DROP TABLE IF EXISTS Backlogs")
    Database.execute_command("DROP TABLE IF EXISTS Cars")

    #Create tables one by one
    create_customer_table()
    create_staff_table()
    create_location_table()
    create_car_table()
    create_booking_table()
    create_backlog_table()
    print("Tables succesfully created")