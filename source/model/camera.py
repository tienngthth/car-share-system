import argparse
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar

class Camera():
    video_stream = None
    frame = None

    @staticmethod
    def scan_code():
        Camera.start_camera()
        # barcodes found thus far
        found_code = set()
        # loop over the frames from the video stream
        while True:
            Camera.grab_frame()
            Camera.validate_code(found_code)
            cv2.imshow("Barcode Scanner", Camera.frame)
            # if the `q` key was pressed, break from the loop
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        Camera.stop_camera()

    @staticmethod
    def start_camera():
        Camera.video_stream = VideoStream(src=0).start()
        time.sleep(2.0)

    @staticmethod
    def grab_frame():
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        Camera.frame = imutils.resize(Camera.video_stream.read(), width=400)

    @staticmethod
    def validate_code(found_code):
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(Camera.frame)
        # loop over the detected barcodes
        for barcode in barcodes:
            # draw a bounding box 
            (x, y, w, h) = barcode.rect
            cv2.rectangle(Camera.frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            barcodeData = barcode.data.decode("utf-8")
            if barcodeData not in found_code:
                print("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))
                found_code.add(barcodeData)
                try:
                    content = json.loads(barcodeData)

    @staticmethod
    def stop_camera():
        cv2.destroyAllWindows()
        Camera.video_stream.stop()

