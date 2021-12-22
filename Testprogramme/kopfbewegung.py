#Programm, dass den Kopf dreht

#!/usr/bin/env phyton3

import RPi.GPIO as GPIO
import time


#Berechnet Motordrehung in Prozent aus dem Drehwinkel aus
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180 

    angle_as_percent = angle * ratio

    return start + angle_as_percent

#Berechnet die einzelnen Teilbewegungen aus und dreht den Motor
def kopfbewegung(posKopf, posPerson):
    t0=0
    ts=0.5
    tend=1
    mittelwert=(posKopf+posPerson)/2
    parabel1=(mittelwert-posKopf)/(ts-t0)**2
    parabel2=(mittelwert-posPerson)/(ts-tend)**2
    x=0
    y=0.5
    for i in range(0,5):
        x+=0.1
        f=parabel1*(x-t0)**2+posKopf
        print(f)
        pwm.ChangeDutyCycle(angle_to_percent(f))
        time.sleep(0.1)

    for i in range(0,5):
        y+=0.1
        f=parabel2*(y-tend)**2+posPerson
        print(f)    
        pwm.ChangeDutyCycle(angle_to_percent(f))
        time.sleep(0.1)


GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings

#Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

#Init at 0°
pwm.start(angle_to_percent(0))
time.sleep(1)


posKopf=0
posPerson=45
a=kopfbewegung(posKopf, posPerson)

#Close GPIO & cleanup
pwm.stop()
GPIO.cleanup()
