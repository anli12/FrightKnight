from gpiozero import LED
import RPi.GPIO as GPIO
#import Adafruit_BBIO.PWM as PWM
import time

red = LED(16)
#pwm.setPWM(pin, 0, 4096);
while True:

    red.on()
    time.sleep(1)
    red.off()
    time.sleep(1)

