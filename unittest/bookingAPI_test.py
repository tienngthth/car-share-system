import unittest
import requests

#Reset the database before running these tests

class Test_Booking_API(unittest.TestCase):
    def test_read(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/read?car_id=1&customer_id=1").json()
        test_data = resp["bookings"][0]     #Change this later by removing "bookings"
        self.assertEqual(test_data["CarID"], 1)
        self.assertEqual(test_data["CustomerID"], 1)
        self.assertEqual(test_data["EventID"], "")
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["RentTime"], "Fri, 21 Aug 2020 10:00:00 GMT")
        self.assertEqual(test_data["ReturnTime"], "Mon, 24 Aug 2020 10:00:00 GMT")
        self.assertEqual(test_data["Status"], "Booked")
        self.assertEqual(test_data["TotalCost"], 144)

    def test_get_profit_data(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/profit/data").json()
        test_data = resp["results"][1]      #Change this later by removing "results"
        self.assertEqual(test_data["Date"], "2020-08-21")
        self.assertEqual(test_data["Total"], 144)

    def test_get_most_profit(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/most/profit").json()
        self.assertEqual(resp["Total"], 7400)
        
    def test_get_bookings_data(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/data").json()
        test_data = resp["results"][0]      #Change this later by removing "results"
        self.assertEqual(test_data["CarID"], 1)
        self.assertEqual(test_data["Total"], 5760)

    def test_get_longest_duration(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/longest/duration").json()
        self.assertEqual(resp["Total"], 15840)

    def test_get_all_customer_bookings(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/all?car_id=1&customer_id=1").json()
        test_data = resp["bookings"][1]     #Change this later by removing "bookings"
        self.assertEqual(test_data["BookingID"], 5)
        self.assertEqual(test_data["CarBrand"], "BMW")
        self.assertEqual(test_data["CarID"], 10)
        self.assertEqual(test_data["RentTime"], "Sun, 23 Aug 2020 14:30:00 GMT")
        self.assertEqual(test_data["ReturnTime"], "Thu, 27 Aug 2020 14:30:00 GMT")
        self.assertEqual(test_data["Status"], "Booked")
        self.assertEqual(test_data["TotalCost"], 192)

    def test_get_customer_bookings_by_time(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/get/by/time?car_id=1&customer_id=1").json()
        test_data = resp["bookings"][1]     #Change this later by removing "bookings"
        self.assertEqual(test_data["BookingID"], 8)
        self.assertEqual(test_data["CarBrand"], "Ford")
        self.assertEqual(test_data["CarID"], 1)
        self.assertEqual(test_data["RentTime"], "Tue, 01 Sep 2020 10:00:00 GMT")
        self.assertEqual(test_data["ReturnTime"], "Wed, 02 Sep 2020 10:00:00 GMT")
        self.assertEqual(test_data["Status"], "Booked")
        self.assertEqual(test_data["TotalCost"], 200)

    def test_remove_customer_from_bookings(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/remove/customer?customer_id=1")
        self.assertEqual(resp.text, "Success")

    def test_remove_car_from_bookings(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/remove/car?car_id=2")
        self.assertEqual(resp.text, "Success")

    def test_create(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/create?customer_id=1&car_id=1&total_cost=50")
        self.assertEqual(resp.text, "Success")

    def test_update(self):
        resp = requests.get("http://127.0.0.1:8080/bookings/update?status=Cancelled&id=1")
        self.assertEqual(resp.text, "Success")

if __name__ == "__main__":
    unittest.main()