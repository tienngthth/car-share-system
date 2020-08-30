from model.client import Client
from model.code import Code

client = None

def send_credential_info():
    credential_message = {
        "message_type":"credential",
        "username":"ABC",
        "password":"123abc",
        "user_type":"customers"
    }
    client.send_message(str(credential_message))
    wait_for_response()

def update_car_status():
    car_status_message = {
        "message_type":"car_status",
        "car_id":"1",
        "car_status":"In use"
    }
    client.send_message(str(car_status_message))
    wait_for_response()

def wait_for_response():
    while True:
        message = client.receive_message()
        if message != "":
            print(message)
            break

def end_connection():
    client.send_message("end")

def listen_to_server():
    update_car_status()
    send_credential_info()
    end_connection()
    
# client.close_socket()
if __name__ == "__main__":
    client = Client()
    listen_to_server() 