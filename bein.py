from adafruit_servokit import ServoKit
import time
import logging

#Parabeln berechnen
def parabel(startzeit, endzeit, startposition, endposition):
    mittelwertpostion=(startposition+endposition)/2
    mittelwertzeit=(startzeit+endzeit)/2
    parabel1=(mittelwertpostion-startposition)/(mittelwertzeit-startzeit)**2
    parabel2=(mittelwertpostion-endposition)/(mittelwertzeit-endzeit)**2
    return(parabel1, parabel2)

#Beindrehung
def beindrehung(angst):
    if angst==True:
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
            time.sleep(0.1)

        for i in range(0,5):
            b+=0.1
            y=parabelwerte[1]*(b-endzeit)**2+endposition
            logging.debug(f"Motor dreht um {y} Grad")
            kit.servo[4].angle = y
            time.sleep(0.1)
    else:
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
            time.sleep(0.5)

        for i in range(0,5):
            b+=0.1
            y=parabelwerte[1]*(b-endzeit)**2+endposition
            logging.debug(f"Motor dreht um {y} Grad")
            kit.servo[4].angle = y
            time.sleep(0.5)

kit = ServoKit(channels=16)

#kit.servo[4].angle = 60
#   time.sleep(5)


angst=True
a=beindrehung(angst)
time.sleep(5)
angst=False
b=beindrehung(angst)
time.sleep(5)
