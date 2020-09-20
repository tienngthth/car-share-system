"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
import unittest
import requests

#Reset the database before running these tests

class TestCustomerAPI(unittest.TestCase):
    def test_read(self):
        resp = requests.get("http://127.0.0.1:8080/customers/read").json()
        test_data = resp[0]       
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["Email"], "tam@gmail.com")
        self.assertEqual(test_data["FirstName"], "Tam")
        self.assertEqual(test_data["LastName"], "Nguyen")
        self.assertEqual(test_data["Phone"], "123456")
        self.assertEqual(test_data["Username"], "tamnguyen")

    def test_get_id(self):
        resp = requests.get("http://127.0.0.1:8080/customers/get/id?username=tamnguyen").json()
        self.assertEqual(resp, 1)

    def test_check_existed_username(self):
        resp = requests.get("http://127.0.0.1:8080/customers/check/existed/username?username=tamnguyen").json()
        self.assertEqual(resp, 1)

    def test_create(self):
        resp = requests.get("http://127.0.0.1:8080/customers/create?username=Tom&password=1234&first_name=Tom&last_name=Nguyen&email=456@gmail.com&phone=1234567")
        self.assertEqual(resp.text, "Success")

    def test_update(self):
        resp = requests.get("http://127.0.0.1:8080/customers/update?customer_id=2&username=Tiennguyen")
        self.assertEqual(resp.text, "Success")

    def test_delete(self):
        resp = requests.get("http://127.0.0.1:8080/customers/delete?id=4")
        self.assertEqual(resp.text, "Success")

if __name__ == "__main__":
    unittest.main()