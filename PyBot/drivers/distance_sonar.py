"""
Driver script of the sonar-distance-sens
generic stuff, there is a lot of infos about this code on beginner sites to raspberry pi. 
no real thinking put into it, only changes made by me:

1. there is a safetytime build in. If one of the signals gets lost most algos drive made. So for this i put in 
a safety time of 0.5 s to stop the meassuring. If no signal comes back in this time, the distance is set to 0
This is super important for the deamon. If a driver fails, we do not see any warnings. the daemon just crashes and thats it
so the drivers need to be safe. Please just change this stuff only with care. 

2. Max Distance is 40cm. every distance above 40 is not reliable or do we have need for it. Always keep in mind, that sonar distance
is the worste distance. 

"""

import time
import pin_belegung as pins
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

sonar = pins.get_sonar()

tR = sonar[0]
eR= sonar[1]
tF = sonar[2]
eF = sonar[3]
tL = sonar[4]
eL = sonar[5]

GPIO.setup(tL, GPIO.OUT)
GPIO.setup(tF, GPIO.OUT)
GPIO.setup(tR, GPIO.OUT)
GPIO.setup(eL, GPIO.IN)
GPIO.setup(eF, GPIO.IN)
GPIO.setup(eR, GPIO.IN)


def distance(side = "front"):
    #for safety fail in daemon. We need to assigne them beforehand
    # and add a safety kill or the daemon will wait forever if the signal
    # gets lost or not detected. Ugly, but working
    StartTime = time.time()
    StopTime = time.time()
    safetyTime = time.time() + 0.5
    
    if side == "front":
        #trigger sonar
        trigger(tF)
        # save starting time
        while GPIO.input(eF) == 0:
            StartTime = time.time()
            
            if(safetyTime < time.time()):
                break
        # save stoptime
        while GPIO.input(eF) == 1:
            StopTime = time.time()
            if(safetyTime < time.time()):
                break
        # get distance by timedifference * time of sound  /2 Ways
    elif side =="left":
        trigger(tL)
        while GPIO.input(eL) == 0:
            StartTime = time.time()
            if(safetyTime < time.time()):
                break
        # save stoptime
        while GPIO.input(eL) == 1:
            StopTime = time.time()
            if(safetyTime < time.time()):
                break
    else:
        trigger(tR)
        while GPIO.input(eR) == 0:
            StartTime = time.time()
            if(safetyTime < time.time()):
                break
        # save stoptime
        while GPIO.input(eR) == 1:
            StopTime = time.time()
            if(safetyTime < time.time()):
                break;

    TimeNeeded = StopTime - StartTime

    distance = (TimeNeeded * 34300) / 2
    
    #if distance is above 40cm is is not messured exactly, so does not matter
    if distance > 40:
        distance = 40
        
    return int(distance)

def trigger(trig):
    GPIO.output(trig, True)
    # wait a sec
    time.sleep(0.0001)
    GPIO.output(trig, False)

