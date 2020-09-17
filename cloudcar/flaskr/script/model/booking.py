from flask import flash

class Booking():
    def __init__(self, car_id, customer_id, rent_time, return_time, cost):
        self.car_id = car_id
        self.customer_id = customer_id
        self.rent_time = rent_time
        self.return_time = return_time
        self.cost = cost
        
    @staticmethod
    def validate_date(start_date, end_date):
        if (end_date - start_date).days < 0:
            flash("End date must be later than start date.")
            return False
        return True

    @staticmethod
    def validate_cost(cost):
        if cost:
            try:
                cost = float(cost)
            except: 
                flash("Cost must be a number.")
                return False
        return True
        
    @staticmethod
    def validate_booking_input(cost, start_date, end_date):
        if Booking.validate_date(start_date, end_date):
            if Booking.validate_cost(cost):
                return True
        return False