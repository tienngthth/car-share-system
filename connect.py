import pymysql

#cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306

def connectToDatabase():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='s3747274',
                                 db='demo_database')
    print("Connected")
    return connection