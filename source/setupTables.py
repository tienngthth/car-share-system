from model.database import Database

def create_customer_table():
    Database.create_table(
        "Customer", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(20), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            PRIMARY KEY(ID)
        ) """
    )
                
def create_staff_table():
    Database.create_table(
        "Staff", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(20), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            UserType VARCHAR(10),
            PRIMARY KEY(ID)
        ) """
    )

def create_car_table():
    Database.create_table(
        "Car", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            MacAddress VARCHAR(30),
            Brand VARCHAR(20),
            Type VARCHAR(20), 
            Location VARCHAR(100), 
            Status VARCHAR(20),
            Color VARCHAR(20),
            Seat INT,
            Cost INT,
            PRIMARY KEY(ID)
        ) """
    )

def create_booking_table():
    Database.create_table(
        "Booking", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            CustomerID INT,
            CarID INT,
            RentTime DATETIME, 
            ReturnTime DATETIME, 
            TotalCost INT,
            PRIMARY KEY(ID),
            FOREIGN KEY (CustomerID) REFERENCES Customer(ID),
            FOREIGN KEY (CarID) REFERENCES Car(ID)
        ) """
    )

def create_backlog_table():
    Database.create_table(
        "Backlog", 
        """ (
            ID INT NOT NULL AUTO_INCREMENT,
            AssignedEngineerID INT,
            SignedEngineerID INT,
            CarID INT,
            Date DATETIME, 
            Status VARCHAR(20),
            Description VARCHAR(100),
            PRIMARY KEY(ID),
            FOREIGN KEY (AssignedEngineerID) REFERENCES Staff(ID),
            FOREIGN KEY (SignedEngineerID) REFERENCES Staff(ID),
            FOREIGN KEY (CarID) REFERENCES Car(ID)
        ) """
    )

def create_all_tables():
    Database.execute_command("DROP TABLE IF EXISTS Booking")
    Database.execute_command("DROP TABLE IF EXISTS Backlog")

    #Create tables one by one
    create_customer_table()
    create_staff_table()
    create_car_table()
    create_booking_table()
    create_backlog_table()
    print("Tables succesfully created")

