class Car():
    def __init__(self, brand, car_type, color, seat, cost):
        self.brand = brand
        self.car_type = car_type
        self.color = color
        self.seat = seat
        self.cost = cost

    @staticmethod
    def validate_cost(cost):
        if cost:
            try:
                cost = float(cost)
            except: 
                return "Cost must be a number"
        return "Valid"



