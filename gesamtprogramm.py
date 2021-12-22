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
from _thread import start_new_thread, allocate_lock



#Motordrehbewegung berechnen
def berechnungMotordrehung(gesicht):
    xmitte=gesicht[0]+((gesicht[2]-gesicht[0])/2)
    print(f"Pixel: {xmitte}")
    posPerson=int(xmitte/(10/3))
    print(f"Winkel Motor: {posPerson}")
    return (posPerson)

#Parabeln berechnen
def parabel(startzeit, endzeit, startposition, endposition):
    mittelwertpostion=(startposition+endposition)/2
    mittelwertzeit=(startzeit+endzeit)/2
    parabel1=(mittelwertpostion-startposition)/(mittelwertzeit-startzeit)**2
    parabel2=(mittelwertpostion-endposition)/(mittelwertzeit-endzeit)**2
    return(parabel1, parabel2)

#Beindrehung
def beindrehung(angst):
    bein=0
    while True:
        if (angst==True) and (bein==0):
            lockBein.acquire()
            startposition=0
            endposition=60
            startzeit=0
            endzeit=1
            parabelwerte=parabel(startzeit,endzeit,startposition,endposition)
            a=0
            b=0.5
            for i in range(0,5):
                a+=0.1
                y=parabelwerte[0]*(a-startzeit)**2+startposition
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[4].angle = y
                time.sleep(0.1)

            for i in range(0,5):
                b+=0.1
                y=parabelwerte[1]*(b-endzeit)**2+endposition
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[4].angle = y
                time.sleep(0.1)
            bein=endposition
            lockBein.release()
        if (angst==False) and (bein==60):
            lockBein.acquire()
            startposition=60
            endposition=0
            startzeit=0
            endzeit=1
            parabelwerte=parabel(startzeit,endzeit,startposition,endposition)
            a=0
            b=0.5
            for i in range(0,5):
                a+=0.1
                y=parabelwerte[0]*(a-startzeit)**2+startposition
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[4].angle = y
                time.sleep(0.5)

            for i in range(0,5):
                b+=0.1
                y=parabelwerte[1]*(b-endzeit)**2+endposition
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[4].angle = y
                time.sleep(0.5)
            bein=endposition
            lockBein.release()

#Mundbewegung
def mundbewegung(angst):
    while angst == True:
        kit.servo[8].angle = 0
        time.sleep(0.5)
        kit.servo[8].angle = 2
        time.sleep(0.5)
        if angst == False:
            break

#Kopfbewegung
def kopfbewegung(angst, gesicht):
    posKopf=0
    while True:
        if angst==True:
            lockKopf.acquire()
            posPerson=berechnungMotordrehung(gesicht)
            startzeit=0
            endzeit=1
            parabelwerte=parabel(startzeit,endzeit,posKopf,posPerson)
            a=0
            b=0.5
            for i in range(0,5):
                a+=0.1
                y=parabelwerte[0]*(a-startzeit)**2+posKopf
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[0].angle = y
                time.sleep(0.1)

            for i in range(0,5):
                b+=0.1
                y=parabelwerte[1]*(b-endzeit)**2+posPerson
                logging.debug(f"Motor dreht um {y} Grad")
                kit.servo[0].angle = y
                time.sleep(0.1)
            posKopf=posPerson
            lockKopf.release()

#logging der Threads
thread_gestartet=False
lockKopf=thread.allocate_lock()
lockBein=thread.allocate_lock()

#Dateien für Gesichtserkennung runterladen
PROTOTXT_FILE_NAME = "deploy.prototxt.txt"
CAFFEMODEL_FILE_NAME = "res10_300x300_ssd_iter_140000.caffemodel"

#Variablen erstellen
gesicht =[]
angst=False


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
#kit.servo[4].set_pulse_width_range(500, 2400) #Beinmotor



#Kamera wird gestartet
logging.info("[INFO] starting video stream...")
vs = VideoStream(src=0, usePiCamera=True,resolution=(320, 240), framerate=32, hflip=False, vflip=True).start()
time.sleep(2) # Nicht löschen! Wichtig für Camera-Setup!

#Threads für die Bewegungen werden gestartet
thread.start_new_thread(kopfbewegung, (angst, gesicht))
thread.start_new_thread(beindrehung, (angst, ))
thread.start_new_thread(mundbewegung, (angst, ))


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
    detections = net.forward() #wenn die KLammer leer ist benutzt es das gesamte Netzwerk

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
    

        #text = "{:.2f}%".format(confidence * 100)
        #y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),
            (0, 0, 255), 2)

        gesicht=box.astype("int")
        if len(gesicht)>3:
            angst=True


        #cv2.putText(frame, text, (startX, y),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    #Bild wird angezeigt, kann später deaktiviert werden
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    #Unterbrechung der Schleife durch Taste "q"
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()
