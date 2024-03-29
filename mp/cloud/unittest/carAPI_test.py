#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests

#Reset the database before running these tests

class TestCarAPI(unittest.TestCase):
    def test_read(self):
        resp = requests.get("http://127.0.0.1:8080/cars/read").json()
        test_data = resp[0]        
        self.assertEqual(test_data["Address"], "RMIT Vietnam, 702 Nguyen Van Linh, Tan Hung, Quan 7, Thanh pho Ho Chi Minh, Vietnam")
        self.assertEqual(test_data["Brand"], "Ford")
        self.assertEqual(test_data["Color"], "White")
        self.assertEqual(test_data["Cost"], 2)
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["MacAddress"], "DC:A6:32:4A:0C:41")
        self.assertEqual(test_data["Seat"], 4)
        self.assertEqual(test_data["Status"], "Unavailable")
        self.assertEqual(test_data["Type"], "Sedan")

    def test_get_available_car(self):
        resp = requests.get("http://127.0.0.1:8080/cars/status/available").json()
        test_data = resp[1]         
        self.assertEqual(test_data["Address"], "Crescent Mall, 101 Ton Dat Tien, Tan Phong, Quan 7, Thanh pho Ho Chi Minh, Vietnam")
        self.assertEqual(test_data["Brand"], "Audi")
        self.assertEqual(test_data["Color"], "Black")
        self.assertEqual(test_data["Cost"], 2)
        self.assertEqual(test_data["ID"], 3)
        self.assertEqual(test_data["MacAddress"], "")
        self.assertEqual(test_data["Seat"], 4)
        self.assertEqual(test_data["Status"], "Available")
        self.assertEqual(test_data["Type"], "Sedan")

    def test_get_car_id_by_mac_address(self):
        resp = requests.get("http://127.0.0.1:8080/cars/get/id?mac_address=DC:A6:32:4A:0C:41").json()
        self.assertEqual(resp, 1)

    def test_get_history(self):
        resp = requests.get("http://127.0.0.1:8080/cars/history?id=1").json()
        test_data = resp[0]        
        self.assertEqual(test_data["CarID"], 1)
        self.assertEqual(test_data["CustomerID"], 1)
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["RentTime"], "Fri, 21 Aug 2020 10:00:00 GMT")
        self.assertEqual(test_data["ReturnTime"], "Mon, 24 Aug 2020 10:00:00 GMT")
        self.assertEqual(test_data["Status"], "Booked")
        self.assertEqual(test_data["TotalCost"], 144)
    
    def test_create(self):
        resp = requests.get("http://127.0.0.1:8080/cars/create?mac_address=&brand=Mercedes&type=Sedan&location_id=1&status=Available&color=White&seat=4&cost=3")
        self.assertEqual(resp.text, "Success")

    def test_update(self):
        resp = requests.get("http://127.0.0.1:8080/cars/update?id=2&cost=4")
        self.assertEqual(resp.text, "Success")

    def test_delete(self):
        resp = requests.get("http://127.0.0.1:8080/cars/delete?id=21")
        self.assertEqual(resp.text, "Success")

if __name__ == "__main__":
    unittest.main()