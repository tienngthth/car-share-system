"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
import pymysql

class Database:
    conn = None
    curs = None

    #Connect to database
    @staticmethod
    def setup_connection():
        Database.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='s3747274',
            db='demo_database',
            cursorclass=pymysql.cursors.DictCursor
        )
        Database.curs = Database.conn.cursor()
     
    #Create a new table
    @staticmethod
    def create_table(tb_name, columns):
        Database.setup_connection()
        Database.curs.execute("DROP TABLE IF EXISTS "+ tb_name)
        Database.curs.execute("CREATE TABLE " + tb_name + columns)
        Database.curs.connection.commit()
        Database.conn.close()

    #Create record 
    @staticmethod
    def insert_record_parameterized(tb_name, values, parameters):
        Database.setup_connection()      
        Database.curs.execute(
            "INSERT INTO " 
            + tb_name 
            + " VALUES" 
            + values
            , parameters
        )
        Database.conn.commit()
        Database.conn.close()

    #Read record
    @staticmethod
    def select_record_parameterized(columns, tb_name, conditions, parameters):
        Database.setup_connection()
        Database.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + tb_name
            + conditions
            , parameters
        )
        return Database.curs.fetchall()

    #Read record
    @staticmethod
    def select_record(columns, tb_name, conditions = ""):
        Database.setup_connection()
        Database.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + tb_name
            + conditions
        )
        return Database.curs.fetchall()

    #Update record 
    @staticmethod
    def update_record_parameterized(tb_name, update_fields, conditions, parameters):
        Database.setup_connection()      
        Database.curs.execute(
            "UPDATE " 
            + tb_name 
            + " SET " 
            + update_fields 
            + conditions
            , parameters
        ) 
        Database.conn.commit()
        Database.conn.close()

    #Delete record 
    @staticmethod
    def delete_record_parameterized(tb_name, conditions, parameters):
        Database.setup_connection()      
        Database.curs.execute(
            "DELETE FROM " 
            + tb_name 
            + conditions
            , parameters
        )
        Database.conn.commit()
        Database.conn.close()

    #Execute a command
    @staticmethod
    def execute_command(command):
        Database.setup_connection()
        Database.curs.execute(command)
        Database.curs.connection.commit()
        Database.conn.close()
