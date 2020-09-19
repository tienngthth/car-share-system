import unittest
import requests

#Reset the database before running these tests

class TestAPI(unittest.TestCase):
    def test_get_user_info(self):
        # We do not test password because it is hashed differently every test
        resp = requests.get("http://127.0.0.1:8080/get/user/info?username=tamnguyen").json()
        self.assertEqual(resp["Email"], "tam@gmail.com")
        self.assertEqual(resp["FirstName"], "Tam")
        self.assertEqual(resp["LastName"], "Nguyen")
        self.assertEqual(resp["Phone"], "123456")
        self.assertEqual(resp["Username"], "tamnguyen")

if __name__ == "__main__":
    unittest.main()