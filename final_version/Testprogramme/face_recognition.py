#Programm, das Gesichter mithilfe der Python Library face recognition erkennt

#!/usr/bin/python3

import cv2
import time
import face_recognition


webcam = cv2.VideoCapture(0)


if webcam.isOpened():
    while True:
        try:
            check, frame = webcam.read()
        
            #cv2.imwrite(filename=name, img=frame)
            #image = face_recognition.load_image_file(name)
            
            #frame = cv2.flip(frame, 0)
            
            face_locations = face_recognition.face_locations(frame)
            for face in face_locations:
                cv2.rectangle(frame, (face[3], face[0]), (face[1], face[2]), (0, 0, 255), 2)

            print(face_locations.__len__())
            cv2.imshow("Capturing", frame)

            print(face_locations)
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

