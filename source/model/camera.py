import argparse
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
from .code import Code

class Camera():
    video_stream = None
    frame = None

    @staticmethod
    def start_camera():
        Camera.video_stream = VideoStream(src=0).start()
        time.sleep(2.0)

    @staticmethod
    def scan_code():
        code = None
        Camera.grab_frame()
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(Camera.frame)
        # loop over the detected barcodes
        for barcode in barcodes:
            Camera.draw_bounding_box(barcode)
            # retrieve and decode content
            code = Code(barcode)
        cv2.imshow("Barcode Scanner", Camera.frame)
        return code 

    @staticmethod
    def grab_frame():
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        Camera.frame = imutils.resize(Camera.video_stream.read(), width=400)

    @staticmethod
    def draw_bounding_box(barcode):
        # draw a bounding box 
        (x, y, w, h) = barcode.rect
        cv2.rectangle(Camera.frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

    @staticmethod
    def stop_camera():
        cv2.destroyAllWindows()
        Camera.video_stream.stop()

