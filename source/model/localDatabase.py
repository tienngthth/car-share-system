import sqlite3
import pathlib

"""
Class Database is to create and connect to the data for recording and retrieving data
"""

class LocalDatabase:
    db_path = pathlib.Path(__file__).parent.parent / "database" / "ap.db"
    tb_name = "ApData"
    conn = None
    curs = None


    #Connect to database
    @staticmethod
    def setup_connection(tb_name, db_path):
        if db_path != None:
            LocalDatabase.db_path = db_path
        if tb_name != None:
            LocalDatabase.tb_name = tb_name
        LocalDatabase.conn = sqlite3.connect(LocalDatabase.db_path)
        LocalDatabase.curs = LocalDatabase.conn.cursor()  

    #Retrieve data by equation
    @staticmethod
    def execute_equation(equation, extra = "", tb_name = None, db_path = None):
        LocalDatabase.setup_connection(tb_name, db_path)
        rows = LocalDatabase.curs.execute(
            "SELECT " 
            + equation
            + " FROM "
            + LocalDatabase.tb_name
            + extra)
        for row in rows:
            return_value = row
        LocalDatabase.conn.close()
        return return_value[0]
        
    #Retrieve data of one record
    @staticmethod
    def select_a_record(columns, extra = "", tb_name = None, db_path = None):
        LocalDatabase.setup_connection(tb_name, db_path)
        rows = LocalDatabase.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + LocalDatabase.tb_name
            + extra
        )
        for row in rows:
            return_value = row
        LocalDatabase.conn.close()
        return return_value

    #Create a new table
    @staticmethod
    def create_table(columns, tb_name = None, db_path = None):
        LocalDatabase.setup_connection(tb_name, db_path)
        LocalDatabase.curs.execute("DROP TABLE IF EXISTS "+ LocalDatabase.tb_name)
        LocalDatabase.curs.execute("CREATE TABLE " + LocalDatabase.tb_name + columns)
        LocalDatabase.conn.close()

    #Update the lastet record in the database
    @staticmethod
    def update_last_record(column, parameter, tb_name = None, db_path = None):
        timestamp = LocalDatabase.execute_equation("MAX(timestamp)")
        LocalDatabase.setup_connection(tb_name, db_path)
        LocalDatabase.curs.execute(
            "UPDATE " 
            + LocalDatabase.tb_name 
            + " set " 
            + column
            + " = (?) WHERE timestamp = '"
            + timestamp
            + "'"
            , parameter
        )
        LocalDatabase.conn.commit()
        LocalDatabase.conn.close()

LocalDatabase.create_table(
    "Username VARCHAR(30), Password VARCHAR(256)", "Credential")