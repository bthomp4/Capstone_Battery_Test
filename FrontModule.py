#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# FrontModule.py
# front module code that receives images and distances from the rear module.
# will display the new image and will light up leds depending on the distances
#
# Green Status LED in the bottom right hand corner. If properly connected stay lit up
# other wise blink
# 1 LED for every 10 feet in front of you.
#
# Ultrasonic related posts:
# http://www.raspberrypi-spy.co.uk/tag/ultrasonic/
#
# Author : Emily Lambert
# Date     : 02/14/2018
# -----------------------

# Python Libraries
import os
import RPi.GPIO as GPIO
from PIL import Image
import time
from random import randint  # delete this later

# GPIO pins and their purpose
GPIO_TRIGGER           = 23    # Trigger for ultrasonic sensor
GPIO_ECHO              = 20    # Echo for ultrasonic sensor
GPIO_LEDSRIGHT         = 21    # LEDS will light up at same time so one GPIO is needed
GPIO_LEDSLEFT          = 27    # LEDS will light up at same time so one GPIO is needed
GPIO_FRONTLED1         = 2
GPIO_FRONTLED2         = 3
GPIO_FRONTLED3         = 4
GPIO_FRONTLED4         = 17
GPIO_FRONTLED5         = 27
GPIO_FRONTLED6         = 22
GPIO_FRONTLED7         = 10
GPIO_FRONTLED8         = 9
GPIO_FRONTLED9         = 11
GPIO_FRONTLED10        = 0

# ---------------------------------------------------
# measure takes a measurement from the front sensor
# ---------------------------------------------------
def measure():
    # This function measures a distance
    GPIO.output(GPIO_TRIGGER, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * speedSound)/2

    return distance

# ---------------------------------------------------
# measure_average finds the average of 3 measurements
# ---------------------------------------------------
def measure_average():
    # This function takes 3 measurements and
    # returns the average.

    distance1=measure()
    time.sleep(0.1)
    distance2=measure()
    time.sleep(0.1)
    distance3=measure()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

def pictureDisplay():
    # Get picture message
    os.system("bash -c 'ping -w 1 umbc.edu'")
    # Display picture
    image = open('test.jpg','wb')   #os.system("bash -c 'xdg-open test.jpg")?
    image_read = image.read()

def updateLEDs():

    print("Distance Recorded at Front Sensor") 
        
    # Get Distance data from front sensor
    distance = measure_average()
    
    print(int(distance), "inches\n")
        
    # Turn on front LEDs as needed
    if distance > 100:
        GPIO.output(GPIO_FRONTLED1, False)
        GPIO.output(GPIO_FRONTLED2, False)
        GPIO.output(GPIO_FRONTLED3, False)
        GPIO.output(GPIO_FRONTLED4, False)
        GPIO.output(GPIO_FRONTLED5, False)
        GPIO.output(GPIO_FRONTLED6, False)
        GPIO.output(GPIO_FRONTLED7, False)
        GPIO.output(GPIO_FRONTLED8, False)
        GPIO.output(GPIO_FRONTLED9, False)
        GPIO.output(GPIO_FRONTLED10, False)
    if distance <= 1200:
        GPIO.output(GPIO_FRONTLED1, True)
    else:
        GPIO.output(GPIO_FRONTLED1, False)
    if distance <= 1080:
        GPIO.output(GPIO_FRONTLED2, True)
    else:
        GPIO.output(GPIO_FRONTLED2, False)
    if distance <= 960:
        GPIO.output(GPIO_FRONTLED3, True)
    else:
        GPIO.output(GPIO_FRONTLED3, False)
    if distance <= 840:
        GPIO.output(GPIO_FRONTLED4, True)
    else:
        GPIO.output(GPIO_FRONTLED4, False)
    if distance <= 720:
        GPIO.output(GPIO_FRONTLED5, True)
    else:
        GPIO.output(GPIO_FRONTLED5, False)
    if distance <= 600:
        GPIO.output(GPIO_FRONTLED6, True)
    else:
        GPIO.output(GPIO_FRONTLED6, False)
    if distance <= 480:
        GPIO.output(GPIO_FRONTLED7, True)
    else:
        GPIO.output(GPIO_FRONTLED7, False)
    if distance <= 360:
        GPIO.output(GPIO_FRONTLED8, True)
    else:
        GPIO.output(GPIO_FRONTLED8, False)
    if distance <= 240:
        GPIO.output(GPIO_FRONTLED9, True)
    else:
        GPIO.output(GPIO_FRONTLED9, False)  
    if distance <= 120:
        GPIO.output(GPIO_FRONTLED10, True)
    else:
        GPIO.output(GPIO_FRONTLED10, False)
        
    # Get distance data from rear module and process
    os.system("bash -c 'ping -w 1 umbc.edu'")
    os.system("bash -c 'ping -w 1 umbc.edu'")
    rightDistance = randint(1,2000) # rand for now later will be obtained from rear
    leftDistance = randint(1,2000) # also a temporary rand
      
    if rightDistance <= 120:
        GPIO.output(GPIO_LEDSRIGHT, True)
    else:
        GPIO.output(GPIO_LEDSRIGHT, False)
    if leftDistance <= 120:
        GPIO.output(GPIO_LEDSLEFT, True)
    else:
        GPIO.output(GPIO_LEDSLEFT, False)
     
    


# ----------------------------------------------------------------------
# Main function that will run all front module processes
# ----------------------------------------------------------------------
def main():
    
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    print("Ultrasonic Measurement")

    # Set pins as output and input 
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)    # Trigger 1
    GPIO.setup(GPIO_ECHO,GPIO.IN)        # Echo 1
    GPIO.setup(GPIO_LEDSRIGHT,GPIO.OUT)
    GPIO.setup(GPIO_LEDSLEFT,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED1,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED2,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED3,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED4,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED5,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED6,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED7,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED8,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED9,GPIO.OUT)
    GPIO.setup(GPIO_FRONTLED10,GPIO.OUT)

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.output(GPIO_LEDSRIGHT, False)
    GPIO.output(GPIO_LEDSLEFT, False)
    GPIO.output(GPIO_FRONTLED1, False)
    GPIO.output(GPIO_FRONTLED2, False)
    GPIO.output(GPIO_FRONTLED3, False)
    GPIO.output(GPIO_FRONTLED4, False)
    GPIO.output(GPIO_FRONTLED5, False)
    GPIO.output(GPIO_FRONTLED6, False)
    GPIO.output(GPIO_FRONTLED7, False)
    GPIO.output(GPIO_FRONTLED8, False)
    GPIO.output(GPIO_FRONTLED9, False)
    GPIO.output(GPIO_FRONTLED10, False)

    # Allow module to settle
    time.sleep(0.5)
    
    # Wrap main content in a try block so we can
    # catch the user pressing CTRL-C and run the
    # GPIO cleanup function. This will also prevent
    # the user seeing lots of unnecessary error
    # messages.
    
    try:
        while True:
            pictureDisplay()
            sleep(0.25)         # sleep for half a second. This may decrease later
            updateLEDs()
            sleep(0.25)         # sleep for half a second. This may decrease later
        
    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        GPIO.cleanup()
        
    
main()