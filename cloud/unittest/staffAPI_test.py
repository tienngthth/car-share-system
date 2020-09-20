#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests

#Reset the database before running these tests

class TestStaffAPI(unittest.TestCase):
    def test_read(self):
        # We do not test password because it is hashed differently every test
        resp = requests.get("http://127.0.0.1:8080/staffs/read").json()
        test_data = resp[0]        
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["Email"], "quoccuong242000@gmail.com")
        self.assertEqual(test_data["FirstName"], "Cuong")
        self.assertEqual(test_data["LastName"], "Nguyen")
        self.assertEqual(test_data["Phone"], "123456")
        self.assertEqual(test_data["Username"], "cuong_nguyen")
        self.assertEqual(test_data["UserType"], "Engineer")
        self.assertEqual(test_data["EngineerMacAddress"], "DC:F7:56:2D:C1:97")

    def test_check_username(self):
        resp = requests.get("http://127.0.0.1:8080/staffs/check/existed/username?username=cuong_nguyen").json()
        self.assertEqual(resp, 1)

    def test_get_enginner_mac_address(self):
        resp = requests.get("http://127.0.0.1:8080/staffs/get/engineer/mac/address?id=1").text
        self.assertEqual(resp, "DC:F7:56:2D:C1:97")

if __name__ == "__main__":
    unittest.main()