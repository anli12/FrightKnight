#Testprogramm für die Bewegungen der Motoren mit Servoboard

#!/usr/bin/python3

from adafruit_servokit import ServoKit
import logging
import time

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
    else:
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
def kopfbewegung(posKopf, posPerson):
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


kit = ServoKit(channels=16)

#Pulsweite der Motoren definieren
#kit.servo[0].set_pulse_width_range(500, 2400) #Kopfmotor
#kit.servo[8].set_pulse_width_range(500, 2400) #Mundmotor
#kit.servo[4].set_pulse_width_range(500, 2400) #Beinmotor

#kit.servo[4].angle = 0
angst = True
a=beindrehung(angst)
#b=mundbewegung(angst)
#time.sleep(10)
#angst = False
#c=beindrehung(angst)
#d=mundbewegung(angst)


