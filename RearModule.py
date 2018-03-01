#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# RearModule.py
# Measure distance using an ultrasonic module
# in a loop.
#
# Ultrasonic related posts:
# http://www.raspberrypi-spy.co.uk/tag/ultrasonic/
#
# Author : Matt Hawkins
# Date     : 16/10/2016
# -----------------------

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import print_function
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import os

# Define GPIO to use on Pi
GPIO_TRIGGER1 = 23
GPIO_ECHO1    = 24
GPIO_TRIGGER2 = 5
GPIO_ECHO2    = 6

# Speed of sound in in/s at temperature
speedSound = 13500 # in/s


# ---------------------------------------------------
# measure1 takes a measurement from the first sensor
# ---------------------------------------------------
def measure1():
    # This function measures a distance
    GPIO.output(GPIO_TRIGGER1, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO1)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO1)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * speedSound)/2

    return distance

# ---------------------------------------------------
# measure_average1 finds the average of 3 measurements
# ---------------------------------------------------
def measure_average1():
    # This function takes 3 measurements and
    # returns the average.

    distance1=measure1()
    time.sleep(0.1)
    distance2=measure1()
    time.sleep(0.1)
    distance3=measure1()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance
 
# ---------------------------------------------------
# measure2 takes a measurement from the second sensor
# --------------------------------------------------- 
def measure2():
    # This function measures a distance
    GPIO.output(GPIO_TRIGGER2, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO2)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO2)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * speedSound)/2

    return distance

# ---------------------------------------------------
# measure_average2 finds the average of 3 measurements
# ---------------------------------------------------
def measure_average2():
    # This function takes 3 measurements and
    # returns the average.

    distance1=measure2()
    time.sleep(0.1)
    distance2=measure2()
    time.sleep(0.1)
    distance3=measure2()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

# ----------------------------------------------------
# Main Script for Side Sensors
# ----------------------------------------------------
def UpdateSideSensors():

    print("Ultrasonic Measurement")

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER1, False)
    GPIO.output(GPIO_TRIGGER2, False)

    # Allow module to settle
    time.sleep(0.5)
    print("Distance Sensor 1\tDistance Sensor 2") 
    distance1 = measure_average1()
    os.system("bash -c 'ping -w 1 umbc.edu'")
    
    distance2 = measure_average2()
    os.system("bash -c 'ping -w 1 umbc.edu'")     
    print(int(distance1), "inches\t\t", int(distance2), "inches")



    
# -----------------------------------------------------------------
# Main Script for taking pictures with the camera
# -----------------------------------------------------------------
def TakePicture(): 

    camera = PiCamera()
    
    camera.start_preview()
        
    #Used to take a still picture
    picture = ('test.jpg') # Made this just test.jpg so we dont overuse memory
    camera.capture(picture)
    os.system("bash -c 'ping -w 1 umbc.edu'")
    camera.stop_preview()
    
    # --------------------------------------------
    # Add code here to send image to front module
    # --------------------------------------------
    
# ----------------------------------------------------------------------
# Main function that will run all rear module processes
# ----------------------------------------------------------------------
def main():
    
    # Wrap main content in a try block so we can
    # catch the user pressing CTRL-C and run the
    # GPIO cleanup function. This will also prevent
    # the user seeing lots of unnecessary error
    # messages.
    
    try:
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        
        # Set pins as output and input 
        GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)    # Trigger 1
        GPIO.setup(GPIO_ECHO1,GPIO.IN)        # Echo 1
        GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)    # Tigger Trigger 2 
        GPIO.setup(GPIO_ECHO2,GPIO.IN)        # ECHO 2
        
        # Set trigger to False (Low)
        GPIO.output(GPIO_TRIGGER1, False)
        GPIO.output(GPIO_TRIGGER2, False)
        
        time.sleep(0.5)                       # allow module to settle

        while True:
            UpdateSideSensors()
            sleep(0.25)                        # 0.25s for now maybe decrease in the end
            TakePicture()
            sleep(0.5)                        # 0.25s for now maybe decrease in the end

    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        GPIO.cleanup()

main()
