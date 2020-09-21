#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests

#Reset the database before running these tests

class TestLocationAPI(unittest.TestCase):
    def test_get_location(self):
        resp = requests.get("http://127.0.0.1:8080/locations/get?id=1").json()
        test_data = resp[0]         
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["Address"], "RMIT Vietnam, 702 Nguyen Van Linh, Tan Hung, Quan 7, Thanh pho Ho Chi Minh, Vietnam")
        self.assertEqual(test_data["Latitude"], 10.729792)
        self.assertEqual(test_data["Longitude"], 106.692107)

if __name__ == "__main__":
    unittest.main()