import pymysql
import connect

def createCustomerTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS Customer")
    cursor.execute(
        "CREATE TABLE Customer ("
            "ID VARCHAR(10) UNIQUE NOT NULL," 
            "Username VARCHAR(30),"
            "Password VARCHAR(20)," 
            "FirstName VARCHAR(20)," 
            "LastName VARCHAR(20),"
            "Email VARCHAR(50)," 
            "PRIMARY KEY(ID)"
        ")"
    )
                
def createStaffTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS Staff")
    cursor.execute(
        "CREATE TABLE Staff ("
            "ID VARCHAR(10) UNIQUE NOT NULL," 
            "Username VARCHAR(30),"
            "Password VARCHAR(20)," 
            "FirstName VARCHAR(20)," 
            "LastName VARCHAR(20),"
            "Email VARCHAR(50)," 
            "UserType VARCHAR(10),"
            "PRIMARY KEY(ID)"
        ")"
    )

def createCarTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS Car")
    cursor.execute(
        "CREATE TABLE Car ("
            "ID VARCHAR(10) UNIQUE NOT NULL," 
            "Brand VARCHAR(20),"
            "Type VARCHAR(20)," 
            "Location VARCHAR(100)," 
            "Status VARCHAR(20),"
            "Color VARCHAR(20),"
            "Seat INT," 
            "Cost INT,"
            "PRIMARY KEY(ID)"
        ")"
    )

def createBookingTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute(
        "CREATE TABLE Booking ("
            "ID VARCHAR(10) UNIQUE NOT NULL,"
            "CustomerID VARCHAR(10)," 
            "CarID VARCHAR(10)," 
            "RentTime DATETIME," 
            "ReturnTime DATETIME," 
            "TotalCost INT,"
            "PRIMARY KEY(ID),"
            "FOREIGN KEY (CustomerID) REFERENCES Customer(ID),"
            "FOREIGN KEY (CarID) REFERENCES Car(ID)"
        ")"
    )

def createBacklogTable(cursor):
    cursor.execute("DROP TABLE IF EXISTS Backlog")
    cursor.execute(
        "CREATE TABLE Backlog ("
            "ID VARCHAR(10) UNIQUE NOT NULL,"
            "EngineerID VARCHAR(10)," 
            "CarID VARCHAR(10)," 
            "Date DATETIME," 
            "Status VARCHAR(20)," 
            "Description VARCHAR(100),"
            "PRIMARY KEY(ID),"
            "FOREIGN KEY (EngineerID) REFERENCES Staff(ID),"
            "FOREIGN KEY (CarID) REFERENCES Car(ID)"
        ")"
    )

def createAllTables():
    #Connect to the database
    cursor = connect.connectToDatabase().cursor()
    #Drop these tables first because they are related to other tables
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("DROP TABLE IF EXISTS Backlog")
    #Create tables one by one
    createCustomerTable(cursor)
    createStaffTable(cursor)
    createCarTable(cursor)
    createBookingTable(cursor)
    createBacklogTable(cursor)
    print("Tables succesfully created")

createAllTables()

