import cv2
from model.code import Code
from model.camera import Camera
from model.database import Database

def validate_code(code, found_codes):
	if code not in found_codes:
		found_codes.add(code)
		try:
			user_info = Code.parse_json(code)
			print(user_info["user_type"])
			if (user_info["user_type"] == "engineer"):
				# close ticket + retrieve engineer info
				# scan QR code -> Engineer ino -> what's next?
				pass
		except:
			pass

def close_backlog():
	backlog = Database.update_record("")

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