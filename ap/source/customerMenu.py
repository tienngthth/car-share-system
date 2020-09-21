from model.util import Util 
from model.customer import Customer
from model.car import car

"""
First Menu for customer login at the begin of the customer bookings
"""
def login_menu():
    escape = False
    while not escape:
        """
        There are two method to login for customer: Facial and Credential. If user press to login as customer by mistake, there is a escape option
        """
        Util.log_messages("login_menu")
        option = Util.get_input("Option: ").lower().strip()
        if option == "e":
            Util.log_messages("back_to_main")
            break
        if option == "f" or option == "c":
            escape = authenticate(option)

def authenticate(option):
    customer = Customer(option)
    if customer.username == "invalid" or customer.password == "invalid":
        Util.log_messages("incorrect_credential")
        return False
    else:
        return customer_menu(customer)

"""
After customer login, this menu will be displayed with the option of locking the car (customer can sign back in) or return car (done with the booking session)
"""
def customer_menu(customer):
    Util.log_messages("customer_menu", (customer.username, ))
    while True:  
        option = Util.get_input("Option: ").lower().strip()
        if option == "l":  
            Util.log_messages("car_locked")
            return False
        elif option == "r": 
            customer.return_car()
            return True

if __name__ == "__main__":
    #check car status (available?)
    login_menu()