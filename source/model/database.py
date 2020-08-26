import pymysql

#To connect to the GCP database:
#1) Download the Cloud SQL Proxy
#2) Download the JSON file included in this project
#3) In the command prompt, navigate to the location of the proxy and run this command:
#cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306 -credential_file=<PATH TO THE JSON FILE>
#4) Ctrl + C to terminate

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
            db='demo_database'
        )
        Database.cursor = Database.conn.cursor()

    #Create a new table
    @staticmethod
    def create_table(tb_name, columns):
        Database.setup_connection()
        Database.curs.execute("DROP TABLE IF EXISTS "+ tb_name)
        Database.curs.execute("CREATE TABLE " + tb_name + columns)
        Database.cursor.connection.commit()
        Database.conn.close()

    #Retrieve record
    @staticmethod
    def select_record(columns, tb_name, extra = ""):
        Database.setup_connection()
        rows = Database.curs.execute(
            "SELECT " 
            + columns 
            + " FROM "
            + tb_name
            + extra
        )
        return_value = []
        for row in rows:
            return_value.append(row)
        Database.conn.close()
        return return_value

    #Insert record 
    @staticmethod
    def insert_record(values, parameters, tb_name):
        Database.setup_connection()      
        Database.curs.execute("INSERT INTO " + tb_name + " values" + values, parameters)
        Database.conn.commit()
        Database.conn.close()

    @staticmethod
    def execute_command(command):
        Database.setup_connection()      
        Database.curs.execute(command)
        Database.conn.commit()
        Database.conn.close()