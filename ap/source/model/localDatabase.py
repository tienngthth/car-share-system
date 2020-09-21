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

    #Create a new table
    @staticmethod
    def create_table(columns, tb_name, db_path = None):
        LocalDatabase.setup_connection(db_path)
        LocalDatabase.curs.execute("DROP TABLE IF EXISTS "+ tb_name)
        LocalDatabase.curs.execute("CREATE TABLE " + tb_name + columns)
        LocalDatabase.conn.close()

    #Insert data record by record
    @staticmethod
    def insert_record(tb_name, values, parameters, db_path = None):
        LocalDatabase.setup_connection(db_path)      
        LocalDatabase.curs.execute("INSERT INTO " + tb_name + " values" + values, parameters)
        LocalDatabase.conn.commit()
        LocalDatabase.conn.close()

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

    @staticmethod
    def select_a_record_parameterized(columns, tb_name, extra, parameters, db_path = None):
        LocalDatabase.setup_connection(db_path)
        rows = LocalDatabase.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + tb_name
            + extra
            , parameters
        )
        for row in rows:
            return_value = row
        LocalDatabase.conn.close()
        return return_value

    #Delete record 
    @staticmethod
    def delete_record(tb_name, conditions, parameters, db_path = None):
        LocalDatabase.setup_connection(db_path)
        LocalDatabase.curs.execute(
            "DELETE FROM " 
            + tb_name 
            + conditions
            , parameters
        )
        LocalDatabase.conn.commit()
        LocalDatabase.conn.close()
