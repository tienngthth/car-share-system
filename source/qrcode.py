import cv2
from model.code import Code
from model.camera import Camera
from model.database import Database
ap_mac_addr = "DC:A6:32:4A:0C:41"
def validate_code(code, found_codes):
	if code not in found_codes:
		found_codes.add(code)
		try:
			user_info = Code.parse_json(code)
			print(user_info["user_type"])
			if (user_info["user_type"] == "engineer"):
				close_backlog(user_info["engineer_id"])
		except:
			pass

# Close ticket and save signed engineer id
def close_backlog(signed_engineer_ID):
	car_id = Database.select_record(" CarID ", " Cars ", " MacAddress = %s", ap_mac_addr)
	Database.update_record(
		" Backlogs ", 
		" signed_engineer_ID = %s, Status = Done ", 
		" CarID = %s"
		,  (signed_engineer_ID, car_id)
	)

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