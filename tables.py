import pymysql, datetime, timedelta
import connect

def create_customer_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Customer")
    cursor.execute("""
        CREATE TABLE Customer (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(20), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            PRIMARY KEY(ID)
        )"""
    )
    cursor.connection.commit()
                
def create_staff_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Staff")
    cursor.execute("""
        CREATE TABLE Staff (
            ID INT NOT NULL AUTO_INCREMENT, 
            Username VARCHAR(30),
            Password VARCHAR(20), 
            FirstName VARCHAR(20), 
            LastName VARCHAR(20),
            Email VARCHAR(50),
            UserType VARCHAR(10),
            PRIMARY KEY(ID)
        )"""
    )
    cursor.connection.commit()

def create_car_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Car")
    cursor.execute("""
        CREATE TABLE Car (
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
        )"""
    )
    cursor.connection.commit()

def create_booking_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("""
        CREATE TABLE Booking (
            ID INT NOT NULL AUTO_INCREMENT,
            CustomerID INT,
            CarID INT,
            RentTime DATETIME, 
            ReturnTime DATETIME, 
            TotalCost INT,
            PRIMARY KEY(ID),
            FOREIGN KEY (CustomerID) REFERENCES Customer(ID),
            FOREIGN KEY (CarID) REFERENCES Car(ID)
        )"""
    )
    cursor.connection.commit()

def create_backlog_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Backlog")
    cursor.execute("""
        CREATE TABLE Backlog (
            ID INT NOT NULL AUTO_INCREMENT,
            EngineerID INT,
            SignedID INT,
            CarID INT,
            Date DATETIME, 
            Status VARCHAR(20),
            Description VARCHAR(100),
            PRIMARY KEY(ID),
            FOREIGN KEY (EngineerID) REFERENCES Staff(ID),
            FOREIGN KEY (SignedID) REFERENCES Staff(ID),
            FOREIGN KEY (CarID) REFERENCES Car(ID)
        )"""
    )
    cursor.connection.commit()

def create_all_tables():
    #Connect to the database
    cursor = connect.connect_to_database().cursor()
    #Drop these tables first because they are related to other tables
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("DROP TABLE IF EXISTS Backlog")
    #Create tables one by one
    create_customer_table(cursor)
    create_staff_table(cursor)
    create_car_table(cursor)
    create_booking_table(cursor)
    create_backlog_table(cursor)
    cursor.close()
    print("Tables succesfully created")

create_all_tables()

