import argparse
import datetime
import imutils
import time
import cv2
import json
from imutils.video import VideoStream
from pyzbar import pyzbar
from model.code import Code

video_stream = None
frame = None

def scan_code():
	start_camera()
	# barcodes found thus far
	found_code = set()
	# loop over the frames from the video stream
	while True:
		grab_frame()
		validate_code(found_code)
		cv2.imshow("Barcode Scanner", frame)
		# if the `q` key was pressed, break from the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
	stop_camera()

def start_camera():
	global video_stream
	video_stream = VideoStream(src=0).start()
	time.sleep(2.0)

def grab_frame():
	global frame, video_stream
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = imutils.resize(video_stream.read(), width=400)

def validate_code(found_code):
	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)
	# loop over the detected barcodes
	for barcode in barcodes:
		# draw a bounding box 
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
		# retrieve and decode content
		code = Code(barcode).decode_content
		print(code)
		print(Code.parse_json(code))
		if code not in found_code:
			found_code.add(code)
			try:
				user_info = Code.parse_json(code)
				if (user_info["user_type"] == "engineer"):
					# close ticket + retrieve engineer info
					# scan QR code -> Engineer ìno -> what's next?
					print("Engineer")
					pass
				print(user_info["user_type"])
			except:
				pass

def stop_camera():
	cv2.destroyAllWindows()
	video_stream.stop()

scan_code()
