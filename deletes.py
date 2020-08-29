import pymysql, datetime, timedelta
import connect

def delete_customer(cursor, ID):
    sql = """DELETE FROM Customers
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_staff(cursor, ID):
    sql = """DELETE FROM Staffs
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_car(cursor, ID):
    sql = """DELETE FROM Cars
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_booking(cursor, ID):
    sql = """DELETE FROM Bookings
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_backlog(cursor, ID):
    sql = """DELETE FROM Backlogs
             WHERE ID = %s"""
    cursor.execute(sql, ID)
    cursor.connection.commit()

def delete_data():
    #Connect to database
    connection = connect.connect_to_database()
    cursor = connection.cursor()

    #Delete data
    delete_customer(cursor, 4)
    delete_staff(cursor, 5)
    delete_car(cursor, 9)
    delete_booking(cursor, 7)
    delete_backlog(cursor, 3)

    #Close connection
    cursor.close()
    connection.close()
    print("Done")

delete_data()