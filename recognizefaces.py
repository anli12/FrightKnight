#!/usr/bin/env phyton3

import cv2
import time
import face_recognition
import RPi.GPIO as GPIO
import time

#Funktion, die den Drehwinkel berechnet
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end =12.5
    ratio = (end - start)/180 #berechnet den Bewegungsanteil von Grad in Prozent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

name="img.jpg"
webcam = cv2.VideoCapture(0) #schaltet die Kamera ein
if webcam.isOpened(): #überprüft ob die Kamera geöffnet ist
    while True:
        try:
            check, frame = webcam.read()
        
            cv2.imwrite(filename=name, img=frame)
            image = face_recognition.load_image_file(name) #nimmt das Bild auf
            face_locations = face_recognition.face_locations(image) #erkennt die Gesichter im Bild
            for face in face_locations:
                cv2.rectangle(frame, (face[3], face[0]), (face[1], face[2]), (0, 0, 255), 2) #erstellt das Rechteck um das Gesicht
                


            print(face_locations.__len__()) #gibt aus wie viele Gesichter zu sehen sind
            cv2.imshow("Capturing", frame) #zeigt Bild an oder nicht (auskomentieren wenn man es in VSCode laufen lässt --> Fehlermeldung)

            print(face_locations) #gibt die Koordinaten des Rechtecks an
                #Motoransteuerung 
            if len(face_locations) > 0:
                    GPIO.setmode(GPIO.BOARD) #benutzt die Numerierung des Boards
                    GPIO.setwarnings(False) #deaktiviert Warnungen

                    #Benutze PIN 12 des PMW Signal --> dieser PIN sendet das Signal an den Motor
                    pwm_gpio = 12
                    frequence = 50
                    GPIO.setup(pwm_gpio, GPIO.OUT)
                    pwm = GPIO.PWM(pwm_gpio, frequence)

                    #Initialisiere den Motor auf 0°
                    pwm.start(angle_to_percent(0))
                    time.sleep(0.1)

                    #Drehe den Motor auf 90°
                    pwm.ChangeDutyCycle(angle_to_percent(90))
                    time.sleep(0.1)

                    #Schließt GPIO & Löscht es
                    pwm.stop()
                    GPIO.cleanup()
                
         
            key = cv2.pollKey()
            if key == ord('q'): #wenn auf der Tastatur q gedrückt wird, endet das Programm
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
        
        except(KeyboardInterrupt): #Program schließt durch einen Keyboardinterrupt
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

