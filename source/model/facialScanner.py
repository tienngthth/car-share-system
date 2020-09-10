import cv2
import numpy as np
import os 
from .camera import Camera
from .util import Util

class FacialScanner():
    names = ['None', 'abcdefg', 'Tien','Tam', 'Minh'] 
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('model/trainer/trainer.yml')

    @staticmethod
    def start_scanning(): 
        id = 0 
        try:
            Camera.start_camera()
            while not Camera.stop:
                faces = Camera.scan_face()
                for(x,y,w,h) in faces:
                    id, confidence = FacialScanner().recognizer.predict(cv2.cvtColor(
                        Camera.frame,
                        cv2.COLOR_BGR2GRAY)[y:y+h,x:x+w]
                    )
                    if (confidence < 80):  
                        Camera.stop_camera()
                        return FacialScanner().names[id]
                Camera.stop_camera_key_stroke()
            return names[0]
        except:
            Util.log_messages("facial_error")

