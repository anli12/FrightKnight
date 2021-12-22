#Dreht alle Motoren auf die Ausgangsposition

from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

kit.servo[0].set_pulse_width_range(500, 2400)
kit.servo[8].set_pulse_width_range(500, 2400)

#Kopfmotor dreht auf Ausgangsposition
kit.servo[0].angle = 40
time.sleep(0.5)

#Mundmotor dreht auf Ausgangsposition
kit.servo[8].angle = 10
time.sleep(0.5)

#Beinmotor dreht auf Ausgangsposition
kit.servo[4].angle = 60
time.sleep(0.5)