from adafruit_servokit import ServoKit
import time



kit = ServoKit(channels=16)

#kit.servo[0].actuation_range = 160
kit.servo[8].set_pulse_width_range(500, 2400)

#Mundbewegung
def mundbewegung():
    while angst == True:
        kit.servo[8].angle = 10
        time.sleep(0.4)
        kit.servo[8].angle = 25
        time.sleep(0.4)
        if angst == False:
            break
        time.sleep(0.01)
        
#kit.servo[8].angle = 15

angst=True
a=mundbewegung()
#kit.servo[0].angle = 40
#time.sleep(0.5)
#kit.servo[8].angle = 60
#time.sleep(0.5)

#kit.servo[3].angle = 0
#kit.servo[4].angle = 0