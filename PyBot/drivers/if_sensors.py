"""
This file manages the TCRT5000 Sensors. 
Theyre used for the cliff left and right and for the wheel encodings. 
the cliff sensors are connected to the mcp23017 and the wheel encoders directly to the pi

no real need of expl. methodes are quite simple. 
"""

import mcp23017 as mcp
import RPi.GPIO as GPIO
import time
import pin_belegung as pins

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


pin = pins.get_cliff_sens()
cliff_sens1 = pin[0]
cliff_sens2 = pin[1]

pin = pins.get_wheel_encoder()
wheel_encoder_left = pin[0]
wheel_encoder_right = pin[1]

mcp.start(0x20)
mcp.setup(cliff_sens1, mcp.IN)
mcp.setup(cliff_sens2, mcp.IN)

GPIO.setup(wheel_encoder_left, GPIO.IN)
GPIO.setup(wheel_encoder_right, GPIO.IN)


def cliff_left():
	if(mcp.input(cliff_sens1)):
		return True
		
	else:
		return False

def cliff_right():
	if(mcp.input(cliff_sens2)):
		return True
		
	else:
		return False

# The wheel counter counts the edges on the pins (high-> low, low -> high)
# therefor we just listen to the pin with an event. for each edge we call a function that does nothing else then 
# increase our global counter. 
# we can reset the counter with an extra methode. this is nessc. if we do stuff with it. if we just change the 
# value on the robot, it does update to the one before after a new update
i = 0
j = 0

# counter workers
def counter_left(channel):
    global i
    i +=1
    
def counter_right():
    global j
    j +=1

#event detect. 
def wheel_count_left():
	GPIO.add_event_detect(wheel_encoder_left, GPIO.BOTH, callback=counter_left)

		
def wheel_count_right():
	GPIO.add_event_detect(wheel_encoder_right, GPIO.BOTH, callback=counter_right)

def wheel_count():
	global i,j
	GPIO.add_event_detect(wheel_encoder_right, GPIO.BOTH, callback=counter_right)
	
	return [i,j]
		
def reset_count():
	global i
	global j
	i = 0
	j = 0
	return True
	


