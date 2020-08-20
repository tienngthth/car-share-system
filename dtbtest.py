import pymysql

#cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306

#Connect
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='s3747274',
                             db='demo_database')
print("Connected")

cursor = connection.cursor()

#Create table
cursor.execute("DROP TABLE IF EXISTS Test_table")
cursor.execute("CREATE TABLE Test_table (Name VARCHAR(255), ID VARCHAR(10))")

#Add rows
sql = "INSERT INTO Test_table (Name, ID) VALUES (%s, %s)"
val = ("Tam", "s3747274")
val2 = ("Minh", "s3651351")
cursor.execute(sql, val)
cursor.execute(sql, val2)

#Get data from table
cursor.execute("SELECT * FROM Test_table")
for x in cursor:
  print(x)