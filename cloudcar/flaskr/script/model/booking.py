from flask import flash

class Booking():
    def __init__(self, car_id, customer_id, rent_time, return_time):
        self.car_id = car_id
        self.customer_id = customer_id
        self.rent_time = rent_time
        self.return_time = return_time
        
    @staticmethod
    def validate_date(start_date, end_date):
        if (end_date - start_date).days < 0:
            return "End date must be later than start date"
        return "Valid"
        