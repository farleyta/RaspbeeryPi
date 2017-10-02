import RPi.GPIO as GPIO

LEFT_TAP_GPIO = 18
RIGHT_TAP_GPIO = 14

GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(LEFT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_TAP_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "start"

leftPulses = 0
rightPulses = 0

def doAClick(channel):
    global leftPulses
    leftPulses += 1
    print "Left pulse: ", leftPulses
    # print "channel: " + channel

def doAClick2(channel):
    global rightPulses
    rightPulses += 1
    print "Right pulse: ", rightPulses

GPIO.add_event_detect(LEFT_TAP_GPIO, GPIO.RISING, callback=doAClick, bouncetime=20) # Left
GPIO.add_event_detect(RIGHT_TAP_GPIO, GPIO.RISING, callback=doAClick2, bouncetime=20) # Right

while True:
    if leftPulses == 10 or rightPulses == 10:
        break
