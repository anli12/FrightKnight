#!/bin/sh
pip3 install  numpy
pip3 install --upgrade picamera[array]  
pip3 install dlib \
    RPi.GPIO \
    imutils \
    logging \
    picamera \
    adafruit-circuitpython-servokit 
pip3 install opencv-python==4.5.3.56