#!/usr/bin/python
import time
import RPi.GPIO as GPIO

from flowmeter import *

LEFT_TAP_GPIO = 18
RIGHT_TAP_GPIO = 14

GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(LEFT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "start"

left = FlowMeter('metric', ["BEER"])
right = FlowMeter('metric', ["WATER"])
minimumPour = 0.1

def countLeftPulses(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if left.enabled == True:
        left.update(currentTime)

def countRightPulses(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if right.enabled == True:
        right.update(currentTime)

GPIO.add_event_detect(LEFT_TAP_GPIO, GPIO.RISING, callback=countLeftPulses, bouncetime=20)
GPIO.add_event_detect(RIGHT_TAP_GPIO, GPIO.RISING, callback=countRightPulses, bouncetime=20)

while True:
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    
    if (left.thisPour > minimumPour and currentTime - left.lastClick > 10000): # 10 seconds of inactivity causes a tweet
        print "Someone just poured " + left.getFormattedThisPour() + " of " + left.getBeverage() 
        left.thisPour = 0.0

    if (right.thisPour > minimumPour and currentTime - right.lastClick > 10000): # 10 seconds of inactivity causes a tweet
        print "Someone just poured " + right.getFormattedThisPour() + " of " + right.getBeverage()
        right.thisPour = 0.0

    # reset flow meter after each pour (2 secs of inactivity)
    if (left.thisPour <= minimumPour and currentTime - left.lastClick > 2000):
        left.thisPour = 0.0
    
    if (right.thisPour <= minimumPour and currentTime - right.lastClick > 2000):
        right.thisPour = 0.0
