#Testprogramm für das Leuchten einer LED

#!/usr/bin/python3

from gpiozero import LED
import time

red = LED(16)

while True:

    red.on()
    time.sleep(1)
    red.off()
    time.sleep(1)

