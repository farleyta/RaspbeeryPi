#!/usr/bin/python
import time
from datetime import datetime
import RPi.GPIO as GPIO

from flowmeter import *
from logPour import logPour

LEFT_TAP_GPIO = 18
RIGHT_TAP_GPIO = 14

GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(LEFT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "start"

# Water 1 - 68725d44-bec8-405a-acda-b558e4a141d5
debug = '00000000-0000-0000-0000-000000000000'
beer = '4cee422a-5f3e-4159-9cf4-f4beab98c08f'
water = '843c059a-76ad-41d1-b3f1-2647785651d4'

left = FlowMeter('metric', [beer]) # beer
right = FlowMeter('metric', [water]) # water
minimumPour = 0.001

def countPulses(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if channel == LEFT_TAP_GPIO:
        if left.enabled == True:
            left.update(currentTime)
    if channel == RIGHT_TAP_GPIO:
        if right.enabled == True:
            right.update(currentTime)

GPIO.add_event_detect(LEFT_TAP_GPIO, GPIO.RISING, callback=countPulses, bouncetime=20)
GPIO.add_event_detect(RIGHT_TAP_GPIO, GPIO.RISING, callback=countPulses, bouncetime=20)

# Simulate a Pour
# logPour(13, '0.13 L', debug, datetime.now(), datetime.now()) 

while True:
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    
    if (left.thisPour > minimumPour and currentTime - left.lastClick > 10000): # 10 seconds of inactivity causes a tweet
        logPour(left.getThisPourInClicks(), left.getFormattedThisPour(), 
                left.getBeverage(), left.pourStarted, left.pourEnded)
        left.finishPour()

    if (right.thisPour > minimumPour and currentTime - right.lastClick > 10000): # 10 seconds of inactivity causes a tweet
        logPour(right.getThisPourInClicks(), right.getFormattedThisPour(),
               right.getBeverage(), right.pourStarted, right.pourEnded)
        right.finishPour()

    # reset flow meter after each pour (2 secs of inactivity)
    if (left.thisPour <= minimumPour and currentTime - left.lastClick > 2000):
        left.finishPour()
    
    if (right.thisPour <= minimumPour and currentTime - right.lastClick > 2000):
        right.finishPour()
