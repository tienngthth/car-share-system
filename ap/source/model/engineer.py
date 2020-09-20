from .car import car
from .code import Code
from .camera import Camera
from .client import Client
from .util import Util

class Engineer():    
    def __init__(self):
        engineer_info = car.get_assgined_engineer_info()
        self.__mac_address = engineer_info["mac_address"]
        self.__engineer_id = engineer_info["engineer_id"]

    def scan_code(self):
        Camera.start_camera()
        # barcodes found thus far
        found_codes = set()
        while not Camera.stop:
            code = Camera.scan_code()
            if code is not None:
                Camera.stop_camera()
                return self.__validate_code(code.decoded_content, found_codes)
            Camera.stop_camera_key_stroke()
        return False

    def __validate_code(self, code, found_codes):
        if code not in found_codes:
            found_codes.add(code)
            try:
                user_info = Code.parse_json(code)
                if (user_info["user_type"] == "engineer"):
                    self.engineer_id = user_info["engineer_id"]
                    return True
            except:
                Util.log_messages("wrong_code")
            return False
    
    def close_backlog(self):
        client = Client()
        message = {
            "message_type" : "close_backlog",
            "engineer_id" : self.engineer_id,
            "car_id" : car.car_id,
            "car_status" : "Available"
        }
        client.send_message(str(message))
        client.send_message("end")
        Util.log_messages("backlog_closed")

    @property
    def engineer_id(self):
        return self.__engineer_id

    @engineer_id.setter
    def engineer_id(self, engineer_id):
        self.__engineer_id = engineer_id

    @property
    def mac_address(self):
        return self.__mac_address

    @mac_address.setter
    def mac_address(self, mac_address):
        self.__mac_address = mac_address


