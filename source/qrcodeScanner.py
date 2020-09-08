import cv2, requests
from model.code import Code
from model.camera import Camera
from model.car import car

ap_mac_addr = "DC:A6:32:4A:0C:41"

def validate_code(code, found_codes):
	if code not in found_codes:
		found_codes.add(code)
		try:
			user_info = Code.parse_json(code)
			if (user_info["user_type"] == "engineer"):
				print("Backlog closed!")
				print(user_info)
				# close_backlog(user_info["engineer_id"])
				return True
		except:
			return False
		return False

# Close ticket and save signed engineer id
def close_backlog(signed_engineer_ID):
	car_id = requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + car.ap_addr
	).text
	requests.put(
		"http://127.0.0.1:8080/backlogs/update/signed/engineer/id/and/status/by/car/id?" +
		"signed_engineer_id=" + signed_engineer_ID +
		"&car_id=" + car_id
	)
	requests.put(
		"http://127.0.0.1:8080/cars/update?" +
		"status=Available" +
		"&id=" + car_id
	)
	print("Done")

def start_scanning():
	Camera.start_camera()
	# barcodes found thus far
	found_codes = set()
	while not Camera.stop:
		code = Camera.scan_code()
		if code is not None:
			if validate_code(code.decoded_content, found_codes):
				Camera.stop_camera()
		Camera.stop_camera_key_stroke()

if __name__ == "__main__":
    start_scanning()
