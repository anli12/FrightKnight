#!/usr/bin/python3

#Importieren der benötigten Libaries
from gpiozero.output_devices import Motor
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import logging
from adafruit_servokit import ServoKit
from picamera import PiCamera
from picamera.array import PiRGBArray
import _thread as thread 
from gpiozero import LED

#initialisieren der LED's
grün=LED(26) #Ground = Pin 39, Spannung = Pin 37
blau=LED(16) #Ground = Pin 34, Spannung = Pin 36

#Grüne LED leuchtet sobald das Programm läuft
grün.on()


#globale Variablen:
gesicht = []
angst = False

#Parabeln berechnen, damit die Gesamtbewegung nicht immer die gleiche Geschwindigkeit hat
def parabel(startzeit, endzeit, startposition, endposition):
    mittelwertpostion=(startposition+endposition)/2
    mittelwertzeit=(startzeit+endzeit)/2
    parabel1=(mittelwertpostion-startposition)/(mittelwertzeit-startzeit)**2
    parabel2=(mittelwertpostion-endposition)/(mittelwertzeit-endzeit)**2
    return(parabel1, parabel2)
    
#Berechnung Zielwert des Kopfes, damit die Person angeschaut wird
def berechnetZielwertKopf(gesicht):
    xmitte=gesicht[0]+((gesicht[2]-gesicht[0])/2)
    print(f"Pixel: {xmitte}")
    posPerson=int(xmitte/(5))
    print(f"Winkel Motor: {posPerson}")
    return (posPerson)

#Welche Person wird verfolge?
def welchePerson(liste):
    if len(liste)==1:
        kopf=liste[0]
        return kopf
    else:
        a=1
        for i in range(len(liste)):
            b=liste[i]
            b2=b[2]
            b1=b[0]
            if a <= (b2-b1):
                a=b2-b1
                kopf=liste[i]
            else:
                c = i
                kopf=liste[c]
        return kopf
    

#Kopfbewegung wird aufgerufen
def kopfbewegung():
    posKopf=0
    motor=0
    while True:
        if angst==True:
            liste = gesicht # Arbeitsvariable, da sonst ein Fehler auftritt, da die Elemente der Liste Gesicht im Hauptthread gelöscht werden
            if len(liste)>0:
                kopf=welchePerson(liste)
                posPerson=berechnetZielwertKopf(kopf)
                posKopf=bewege_beinkopf(motor, posKopf, posPerson, delay=0.1)
                logging.debug("Kopf dreht")

        time.sleep(.01)

#Bewegungen des Beines und des Kopfes wird ausgeführt
def bewege_beinkopf(motor, startposition, endposition, delay, startzeit=0, endzeit=1):
    parabelwerte=parabel(startzeit, endzeit, startposition, endposition)
    a=0
    b=0.5
    for i in range(0,5):
        a+=0.1
        y=parabelwerte[0]*(a-startzeit)**2+startposition
        kit.servo[motor].angle = y
        time.sleep(delay)

    for i in range(0,5):
        b+=0.1
        y=parabelwerte[1]*(b-endzeit)**2+endposition
        kit.servo[motor].angle = y
        time.sleep(delay)
        
    return endposition


#Beindrehung wird aufgerufen
def beindrehung():
    bein=60
    motor=4
    while True:
        if (angst==True) and (bein==60):
            bein = bewege_beinkopf(motor,60, 1, delay=0.1)
            kit.servo[4].angle=5
            logging.debug("Bein dreht")

        if (angst==False) and (bein==1):
            bein = bewege_beinkopf(motor,1, 60, delay=0.5)
            kit.servo[4].angle=50
            logging.debug("Bein dreht")

        time.sleep(0.01)


#Mundbewegung
def mundbewegung():
    while True:
        if angst == True:
            kit.servo[8].angle = 10
            time.sleep(5)
            kit.servo[8].angle = 15
            time.sleep(5)
            logging.debug("Mund bewegt sich")

            
        time.sleep(0.01)



#Dateien für Gesichtserkennung runterladen
PROTOTXT_FILE_NAME = "deploy.prototxt.txt"
CAFFEMODEL_FILE_NAME = "res10_300x300_ssd_iter_140000.caffemodel"


logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s")

#Erstellung des Dictionarys für die Gesichtserkennung
args = {
    "prototxt": PROTOTXT_FILE_NAME,
    "model": CAFFEMODEL_FILE_NAME,
    "confidence": 0.5
}

logging.info("[INFO] loading model...")

net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#Servoboard und Motoren initialisieren
kit = ServoKit(channels=16)

#Pulsweite der Motoren definieren
kit.servo[0].set_pulse_width_range(500, 2400) #Kopfmotor
kit.servo[8].set_pulse_width_range(500, 2400) #Mundmotor


#Ausgangsposition der Motoren einstellen
kit.servo[0].angle = 40
kit.servo[4].angle = 60
kit.servo[8].angle = 10


#Kamera wird gestartet
logging.info("[INFO] starting video stream...")
vs = VideoStream(src=0, usePiCamera=True,resolution=(320, 240), framerate=32, hflip=False, vflip=True).start()
time.sleep(2) # Nicht löschen! Wichtig für Camera-Setup!

#Threads für die Bewegungen werden gestartet
thread.start_new_thread(kopfbewegung,())
thread.start_new_thread(beindrehung,())
thread.start_new_thread(mundbewegung,())


#Endlosschleife über die Bilder des Videos der Kamera
while True:
    logging.debug("Grabbing image")
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
 
    #Bild wird in das blob Format konvertiert
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0)) #erstellt einen 4-dimensionalen blob von dem Bild
        
 
    #Gesichter werden erkannt
    net.setInput(blob) #gibt den neuen Input für das Netzwerk
    detections = net.forward() #wenn die Klammer leer ist benutzt es das gesamte Netzwerk

    #Liste über Gesichter wird für das nächste Bild gelehrt
    del gesicht[0:len(gesicht)]

    #for-Schleife über die erkannten Gesichter
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        #schlechte Gesichterkennungsergebnisse werden herausgefiltert
        if confidence < args["confidence"]:
            continue

            
        #Box um die Gesichter wird erstellt
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        logging.debug(f"Detected face at {(startX, startY, endX, endY)}.")
    

        cv2.rectangle(frame, (startX, startY), (endX, endY),
            (0, 0, 255), 2)

        gesicht.append(box.astype("int"))


    #Bild wird angezeigt, kann später deaktiviert werden
    cv2.imshow("Frame", frame)

    if len(gesicht)>0:
        angst=True
        blau.on()
    else:
        angst=False
        blau.off()

    key = cv2.waitKey(1) & 0xFF
 
    #Unterbrechung der Schleife durch Taste "q"
    if key == ord("q"):
        break

grün.off()
blau.off()
cv2.destroyAllWindows()
vs.stop()