from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import logging
from picamera import PiCamera
from picamera.array import PiRGBArray

#Dateien für Gesichtserkennung runterladen
PROTOTXT_FILE_NAME = "deploy.prototxt.txt"
CAFFEMODEL_FILE_NAME = "res10_300x300_ssd_iter_140000.caffemodel"

gesicht=[]
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s")

#Erstellung des Dictionarys für die Gesichtserkennung
args = {
	"prototxt": PROTOTXT_FILE_NAME,
	"model": CAFFEMODEL_FILE_NAME,
	"confidence": 0.5
}

logging.info("[INFO] loading model...")

net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#Kamera wird gestartet
logging.info("[INFO] starting video stream...")
vs = VideoStream(src=0, usePiCamera=True,resolution=(320, 240), framerate=32, hflip=False, vflip=True).start()
time.sleep(2) # Nicht löschen! Wichtig für Camera-Setup!


#Schleife über die Bilder des Videos der Kamera
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