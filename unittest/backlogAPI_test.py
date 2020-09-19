import unittest
import requests

#Reset the database before running these tests

class Test_Backlog_API(unittest.TestCase):
    def test_get_backlogs_data(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/get/backlogs/data").json()
        test_data = resp[0]
        self.assertEqual(test_data["CarID"], 1)
        self.assertEqual(test_data["Total"], 1)

    def test_get_all(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/get/all").json()
        test_data = resp["backlogs"][0]         #Change this later by removing "backlogs"
        self.assertEqual(test_data["CarBrand"], "Audi")
        self.assertEqual(test_data["CarID"], 3)
        self.assertEqual(test_data["CarType"], "Sedan")
        self.assertEqual(test_data["Description"], "Car ran out of fuel")
        self.assertEqual(test_data["LocationID"], 2)
        self.assertEqual(test_data["Status"], "Done")

    def test_get_engineer_id(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/get/engineer/id?car_id=7").json()
        self.assertEqual(resp["AssignedEngineerID"], 1)

    def test_create(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/create?assigned_engineer_id=1&car_id=1&status=Not%20done&description=Change%20the%20tires")
        self.assertEqual(resp.text, "Success")

    def test_close(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/close?signed_engineer_id=1&car_id=1")
        self.assertEqual(resp.text, "Success")
        
    def test_remove_assigned_engineer(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/remove/assigned/engineer?id=1")
        self.assertEqual(resp.text, "Success")

    def test_remove_signed_engineer(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/remove/signed/engineer?id=3")
        self.assertEqual(resp.text, "Success")

    def test_remove_car(self):
        resp = requests.get("http://127.0.0.1:8080/backlogs/remove/car?car_id=18")
        self.assertEqual(resp.text, "Success")

if __name__ == "__main__":
    unittest.main()