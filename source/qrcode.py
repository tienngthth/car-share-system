import cv2, requests
from model.code import Code
from model.camera import Camera

ap_mac_addr = "DC:A6:32:4A:0C:41"

def validate_code(code, found_codes):
	if code not in found_codes:
		found_codes.add(code)
		user_info = Code.parse_json(code)
		if (user_info["user_type"] == "engineer"):
			close_backlog(user_info["engineer_id"])

# Close ticket and save signed engineer id
def close_backlog(signed_engineer_ID):
	car_id = requests.get(
		"http://127.0.0.1:8080/cars/get/car/id/by/mac/address?" +
		"mac_address=" + ap_mac_addr
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
	while True:
		code = Camera.scan_code()
		if code is not None:
			validate_code(code.decoded_content, found_codes)
		# if the `q` key was pressed, break from the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
	Camera.stop_camera()

if __name__ == "__main__": 
    start_scanning()