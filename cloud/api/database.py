#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py handles the connection to the Google Cloud DB, and contains helper functions for modifying entries that are used widely in this application.
"""
import pymysql

class Database:
    conn = None
    curs = None

    #Connect to database
    @staticmethod
    def setup_connection():
        """
        The details of the Google Cloud DB. It uses a local proxy to connect, it is not actually running on localhost.
        """
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
        """
        This creates a table. Parameters:
        
        tb_name: The table name
        columns: The columns that belong in this table
        
        Returns nothing.
        """
        Database.setup_connection()
        Database.curs.execute("DROP TABLE IF EXISTS "+ tb_name)
        Database.curs.execute("CREATE TABLE " + tb_name + columns)
        Database.curs.connection.commit()
        Database.conn.close()

    #Create record 
    @staticmethod
    def insert_record_parameterized(tb_name, values, parameters):
        """
        Helper function to insert a DB record. Parameters:
        
        tb_name: The name of the table
        values: A list of columns to insert the data into
        parameters: The actual data to insert
        
        Returns nothing.
        """
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
        """
        Helper function to select DB records. Parameters:
        
        columns: The columns to return
        tb_name: The name of the table
        condidtions: the SELECT conditions
        parameters: The actual data to search by
        
        Returns any rows found
        """
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
        """
        Same as select_record_parameterized() but returns all rows instead of searching with some criteria.
        """
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
        """
        Same as insert_record_parameterized, but performs an UPDATE operation istead of an INSERT.
        """
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
        """
        Helper function to delete a record. Parameters:
        
        tb_name: the table to delete from.
        conditions: The conditions we will use to find which rows to delete
        parameters: The actual data used to find rows to delete
        
        Returns nothing.
        """
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
        """
        This initializes the database.
        """
        Database.setup_connection()
        Database.curs.execute(command)
        Database.curs.connection.commit()
        Database.conn.close()
