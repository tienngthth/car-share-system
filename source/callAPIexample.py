import requests
import json

data_send = None

# Function to call GET API to get the latest context from the database
def test_1():
    resp = requests.get('http://127.0.0.1:8080/bookings/get/booking/by/customer/or/car/id?customer_id=1')
    print(resp.text)

# Function to call GET API to get the latest context from the database
def test_2():
    resp = requests.get('http://127.0.0.1:8080/cars/create/car?mac_address=&brand=ABC&type=&location=&status=to%20be%20repaired&color=&seat=5&cost=50')
    print(resp.text)


test_1()
test_2()