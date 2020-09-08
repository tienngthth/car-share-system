import argparse
import datetime
import imutils
import time
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
from .code import Code

class Camera():
    cam = None
    frame = None
    width = 480
    height = 640
    stop = False

    @staticmethod
    def start_camera():
        Camera.cam = cv2.VideoCapture(0)
        Camera.cam.set(3, 640)
        Camera.cam.set(4, 480)
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
    def draw_bounding_box(barcode):
        # draw a bounding box 
        (x, y, w, h) = barcode.rect
        cv2.rectangle(Camera.frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

    @staticmethod
    def scan_face():
        Camera.grab_frame()
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale( 
            cv2.cvtColor(Camera.frame, cv2.COLOR_BGR2GRAY),
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(0.1*Camera.cam.get(3)), int(0.1*Camera.cam.get(4)))
        )
        cv2.imshow("Face Scanner", Camera.frame) 
        return faces

    @staticmethod
    def grab_frame():
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        ret, Camera.frame = Camera.cam.read()

    @staticmethod
    def stop_camera_key_stroke():
        if not Camera.stop:
            # Press 'ESC' for exiting video
            k = cv2.waitKey(10) & 0xff 
            if k == 27:
                Camera.stop_camera()

    @staticmethod
    def stop_camera():
        Camera.cam.release()
        cv2.destroyAllWindows()
        Camera.stop = True