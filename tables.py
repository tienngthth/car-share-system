import pymysql, datetime, timedelta
import connect

def create_customers_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Customers")
    cursor.execute("""
        CREATE TABLE Customers (
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
                
def create_staffs_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Staffs")
    cursor.execute("""
        CREATE TABLE Staffs (
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

def create_cars_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Cars")
    cursor.execute("""
        CREATE TABLE Cars (
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

def create_bookings_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Bookings")
    cursor.execute("""
        CREATE TABLE Bookings (
            ID INT NOT NULL AUTO_INCREMENT,
            CustomerID INT,
            CarID INT,
            RentTime DATETIME, 
            ReturnTime DATETIME, 
            TotalCost INT,
            PRIMARY KEY(ID),
            FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
            FOREIGN KEY (CarID) REFERENCES Cars(ID)
        )"""
    )
    cursor.connection.commit()

def create_backlogs_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS Backlogs")
    cursor.execute("""
        CREATE TABLE Backlogs (
            ID INT NOT NULL AUTO_INCREMENT,
            EngineerID INT,
            SignedID INT,
            CarID INT,
            Date DATETIME, 
            Status VARCHAR(20),
            Description VARCHAR(100),
            PRIMARY KEY(ID),
            FOREIGN KEY (EngineerID) REFERENCES Staffs(ID),
            FOREIGN KEY (SignedID) REFERENCES Staffs(ID),
            FOREIGN KEY (CarID) REFERENCES Cars(ID)
        )"""
    )
    cursor.connection.commit()

def create_all_tables():
    #Connect to the database
    connection = connect.connect_to_database()
    cursor = connection.cursor()
    #Drop these tables first because they are related to other tables
    cursor.execute("DROP TABLE IF EXISTS Bookings")
    cursor.execute("DROP TABLE IF EXISTS Backlogs")
    #Create tables one by one
    create_customers_table(cursor)
    create_staffs_table(cursor)
    create_cars_table(cursor)
    create_bookings_table(cursor)
    create_backlogs_table(cursor)

    #CLose connection
    cursor.close()
    connection.close()
    print("Tables succesfully created")

create_all_tables()

