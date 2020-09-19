import unittest
import requests

#Reset the database before running these tests

class TestLocationAPI(unittest.TestCase):
    def test_get_location(self):
        resp = requests.get("http://127.0.0.1:8080/locations/get?id=1").json()
        test_data = resp["location"][0]         #Change this later by removing "location"
        self.assertEqual(test_data["ID"], 1)
        self.assertEqual(test_data["Address"], "RMIT Vietnam, 702 Nguy\u1ec5n V\u0103n Linh, T\u00e2n H\u01b0ng, Qu\u1eadn 7, Th\u00e0nh ph\u1ed1 H\u1ed3 Ch\u00ed Minh, Vietnam")
        self.assertEqual(test_data["Latitude"], 10.729792)
        self.assertEqual(test_data["Longitude"], 106.692107)

if __name__ == "__main__":
    unittest.main()