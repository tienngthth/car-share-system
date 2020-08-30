from model.client import Client

client = Client()

credential_message = {
    "message_type":"credential",
    "username":"tien123N",
    "password":"123",
    "user_type":"customers"

}
car_status_message = {
    "message_type":"car_status",
    "car_id":"1",
    "status":"In use"
}

client.send_message(credential_message)
client.send_message(car_status_message)

client.close_socket()
