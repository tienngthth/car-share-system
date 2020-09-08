import sqlite3
import pathlib

"""
Class Database is to create and connect to the data for recording and retrieving data
"""

class LocalDatabase:
    db_path = "databases/ap.db"
    conn = None
    curs = None

    #Connect to database
    @staticmethod
    def setup_connection(db_path):
        if db_path != None:
            LocalDatabase.db_path = db_path
        LocalDatabase.conn = sqlite3.connect(LocalDatabase.db_path)
        LocalDatabase.curs = LocalDatabase.conn.cursor()  

    #Retrieve data by equation
    @staticmethod
    def execute_equation(equation, tb_name, extra = "", db_path = None):
        LocalDatabase.setup_connection(db_path)
        rows = LocalDatabase.curs.execute(
            "SELECT " 
            + equation
            + " FROM "
            + tb_name
            + extra)
        for row in rows:
            return_value = row
        LocalDatabase.conn.close()
        return return_value[0]
        
    #Retrieve data of one record
    @staticmethod
    def select_a_record(columns, tb_name, extra = "", db_path = None):
        LocalDatabase.setup_connection(db_path)
        rows = LocalDatabase.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + tb_name
            + extra
        )
        for row in rows:
            return_value = row
        LocalDatabase.conn.close()
        return return_value

    #Create a new table
    @staticmethod
    def create_table(columns, tb_name, db_path = None):
        LocalDatabase.setup_connection(db_path)
        LocalDatabase.curs.execute("DROP TABLE IF EXISTS "+ tb_name)
        LocalDatabase.curs.execute("CREATE TABLE " + tb_name + columns)
        LocalDatabase.conn.close()

    #Update the lastet record in the database
    @staticmethod
    def update_last_record(tb_name, column, parameter, db_path = None):
        timestamp = LocalDatabase.execute_equation("MAX(timestamp)", tb_name)
        LocalDatabase.setup_connection(db_path)
        LocalDatabase.curs.execute(
            "UPDATE " 
            + tb_name 
            + " set " 
            + column
            + " = (?) WHERE timestamp = '"
            + timestamp
            + "'"
            , parameter
        )
        LocalDatabase.conn.commit()
        LocalDatabase.conn.close()

# LocalDatabase.create_table("(Username VARCHAR(30), Password VARCHAR(256))", "Credential ")