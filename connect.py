import pymysql

#To connect to the GCP database:
#1) Download the Cloud SQL Proxy
#2) Download the JSON file included in this project
#3) In the command prompt, navigate to the location of the proxy and run this command:
#cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306 -credential_file=<PATH TO THE JSON FILE>

def connectToDatabase():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='s3747274',
                                 db='demo_database')
    print("Connected")
    return connection