#!/usr/bin/env phyton3

import cv2
import time
import face_recognition

name="img.jpg"
webcam = cv2.VideoCapture(0)
if webcam.isOpened():
    while True:
        try:
            check, frame = webcam.read()
        
            #cv2.imwrite(filename=name, img=frame)
            #image = face_recognition.load_image_file(name)
            image = frame
            
            face_locations = face_recognition.face_locations(image)
            for face in face_locations:
                cv2.rectangle(frame, (face[3], face[0]), (face[1], face[2]), (0, 0, 255), 2)


            print(face_locations.__len__())
            cv2.imshow("Capturing", frame)

            print(face_locations)           
            key = cv2.pollKey()
            if key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

