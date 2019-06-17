"""
This script is an overlay for our l293d driver
is needed for the multi-processing of driving functions in the view and robot

each direction is called with the same args: 
time to drive, power left, power right

"""

import l293d_own
import time
import RPi.GPIO as GPIO
import threading

#motor 1 pins: 16,18,22
#motor 2 pins: 36,38,40
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#motor1 = left

motor1 = l293d_own.DC(40,38,36)
motor2 = l293d_own.DC(22,16,18)

def backward(t=0.1,s_left=100,s_right=100):
	backward_thread = threading.Thread(target=backward_worker, args=(t,s_left, s_right))
	backward_thread.setDaemon(True)
	backward_thread.start()
	
def backward_worker(t=0.1,s_left=100,s_right=100):
	motor1.clockwise(speed=s_right)
	motor2.clockwise(speed=s_left)
	time.sleep(t)
	stop()

def forward(t=0.1,s_left=85,s_right=100):
	forward_thread = threading.Thread(target=forward_worker, args=(t,s_left, s_right))
	forward_thread.setDaemon(True)
	forward_thread.start()

def forward_worker(t=0.1,s_left=80,s_right=100):
	motor1.anticlockwise(speed=s_right)
	motor2.anticlockwise(speed=s_left)
	time.sleep(t)
	stop()

def rightturn(t=0.1,s_left=80,s_right=100):
	rightturn_thread = threading.Thread(target=rightturn_worker, args=(t,s_left, s_right))
	rightturn_thread.setDaemon(True)
	rightturn_thread.start()

def rightturn_worker(t=0.1,s_left=100,s_right=100):
	motor1.clockwise(speed=s_right)
	motor2.anticlockwise(speed=s_left)
	time.sleep(t)
	stop()

def leftturn(t=0.1,s_left=100,s_right=100):
	leftturn_thread = threading.Thread(target=leftturn_worker, args=(t,s_left, s_right))
	leftturn_thread.setDaemon(True)
	leftturn_thread.start()
	
def leftturn_worker(t=0.1,s_left=100,s_right=100):
	motor1.anticlockwise(speed=s_right)
	motor2.clockwise(speed=s_left)
	time.sleep(t)
	stop()
	
def stop():
	motor1.stop()
	motor2.stop()

def square():
	square_thread = threading.Thread(name="square_daemon", target=square_worker)
	square_thread.setDaemon(True)
	square_thread.start()
	
def square_worker():
	for i in range(4):
		forward_worker(0.4)
		leftturn_worker(0.35)
		time.sleep(0.1)

def circle():
	circle_thread = threading.Thread(name="circle_daemon", target=circle_worker)
	circle_thread.setDaemon(True)
	circle_thread.start()
	
		
def circle_worker():
	forward(2,5,100)

