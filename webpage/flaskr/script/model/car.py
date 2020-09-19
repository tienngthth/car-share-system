from flask import flash
import requests

class Car():
    def __init__(self, brand, car_type, color, seat, cost, location_id, mac_address="", status = "Available"):
        self.brand = brand
        self.car_type = car_type
        self.color = color
        self.seat = seat
        self.cost = cost
        self.mac_address = mac_address
        self.status = status
        self.location_id = location_id

    @staticmethod
    def validate_cost(cost):
        if cost:
            try:
                cost = float(cost)
                if cost > 1000 or cost < 1:
                    flash("Cost must be between 1 and 1000.")
                    return False
            except: 
                flash("Cost must be a number")
                return False
        return True

    @staticmethod   
    def validate_location_id(location_id):
        if location_id:
            try:
                location_id = int(location_id)
            except: 
                flash("Location id must be a number")
                return False
        return True

    def validate_new_car(self):
        if Car.validate_cost(self.cost) and Car.validate_location_id(self.location_id):
            return True
        return False

    def validate_update_car(self):
        if self.cost != "" and not Car.validate_cost(self.cost):
            return False
        return Car.validate_location_id(self.location_id)

    def create_car(self):
        requests.post(
            "http://127.0.0.1:8080/cars/create?" +
            "mac_address=" + self.mac_address +
            "&brand=" + self.brand + 
            "&type=" + self.car_type +
            "&location_id=" + self.location_id +
            "&status=Available" + 
            "&color=" + self.color +
            "&seat=" + self.seat +
            "&cost=" + self.cost
        )
        flash("New car created!")

    def update_car(self, car_id):
        requests.put(
            "http://127.0.0.1:8080/cars/update?" +
            "mac_address=" + self.mac_address +
            "&brand=" + self.brand + 
            "&type=" + self.car_type +
            "&location_id=" + self.location_id +
            "&status=" + self.status +
            "&color=" + self.color +
            "&seat=" + self.seat +
            "&cost=" + self.cost +
            "&id=" + car_id

        )
        flash("Car updated!")