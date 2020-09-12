import requests

# Function to call GET API to get the latest context from the database
def test_1():
    resp = requests.get('http://127.0.0.1:8080/bookings/get/booking/by/customer/or/car/id?customer_id=1')
    print(resp.text)

# Function to call GET API to get the latest context from the database
def test_2():
    resp = requests.get('http://127.0.0.1:8080/cars/create?mac_address=&brand=ABC&type=&latitude=&longitude=&status=to%20be%20repaired&color=&seat=5&cost=50')
    print(resp.text)

car = requests.get("http://127.0.0.1:8080/cars/get/car/by/ID?id=1").json()
print(car["car"])