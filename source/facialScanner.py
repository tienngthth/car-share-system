import cv2
import numpy as np
import os 
from model.camera import Camera

id = 0
names = ['None', 'abc', 'Tien','Tam', 'Minh'] 
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

def start_scanning():  
    Camera.start_camera()
    while not Camera.stop:
        faces = Camera.scan_face()
        for(x,y,w,h) in faces:
            id, confidence = recognizer.predict(cv2.cvtColor(
                Camera.frame,
                cv2.COLOR_BGR2GRAY)[y:y+h,x:x+w]
            )
            if (confidence < 80):  
                print(names[id])
                Camera.stop_camera()
                return names[id]
        Camera.stop_camera_key_stroke()
    return names[0]

if __name__ == "__main__":
    start_scanning()

