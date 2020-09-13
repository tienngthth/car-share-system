# Car-Share-System
#Instruction

To connect to the GCP database:
* Download the Cloud SQL Proxy (go to https://cloud.google.com/sql/docs/mysql/sql-proxy)
* Download the clean-wonder-286803-fd26772409c0.json file included in this project (located in source/files)
* In the command prompt, navigate to the location of the proxy and run this command:
cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306 -credential_file=<PATH TO THE JSON FILE>
* Ctrl + C to terminate when done

To view the graphs:
* Connect to the GCP database
* Run the file api.py
* Open the browser and run the APIs in graphAPI.py:
http://127.0.0.1:8080/graphs/most/booked/cars
http://127.0.0.1:8080/graphs/most/repaired/cars
http://127.0.0.1:8080/graphs/profit/by/date 



