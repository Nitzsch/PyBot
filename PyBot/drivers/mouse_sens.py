"""
This file cost me so much energy. 
it is a driver for the ADNS-2610 from Avago. An Opti-Flow-Sensor or so called Mouse-Sensor

I read the docs of the sensor about 10 times. so... yeah. and this is the result

Most important methodes: 
1. dy(), dx(): 
    this Methodes return the value of the changes in the x-y-Frame
    remember: the range is only -128 to 127 so call this stuff fast and frequent. 
    if you do not do this, you get lost. The space on the disc just stops on 127 and you do not know where you are
    after each call of dx(), dy() the disc space gets resetted to 0. 
    time for another loop 
    also: the return value is a list!!!! and it has in it the bit values. not an int. for that you need to call:
2. fromSensToInt(dx() or dy()):
    this methode calculates an int value of the readings from dx, dy. 
    nothing more. 

If you need help how to call this stuff, look at the end of the file. you will find some examples. 
Most other Methodes are of little to no use. I mean... you can look at the greyscale pic of the adns. great. 
If you really want to implement a scanner with that: go ahead. 

"""

import time
import RPi.GPIO as GPIO
import pin_belegung as pins

pin= pins.get_mouse_sensor()
#set Pins
scklPin = pin[1]
scdioPin = pin[0]

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#setup clock, it starts high!
GPIO.setup(scklPin, GPIO.OUT, initial=GPIO.HIGH)
#First act is always sending out data to controller
#therefore sckl is out
GPIO.setup(scdioPin, GPIO.OUT)

#the controller always needs to sync first
# this is done by sending 1-0-1 via clock and waiting 1 sec
#starts high, so first is low
def resync():
    GPIO.output(scklPin, GPIO.LOW)
    #followed by high
    GPIO.output(scklPin, GPIO.HIGH)
    # wait
    time.sleep(0.1)

# read Data funct
# needs address list. has to be 8 bits long. Contains only 0 or 1
# first bit hast to be 0 to signal reading op to controller
# returns 8 bits of info
def readData(adr):
    #sync pi and controller
    resync()
    data=[]
    #First act is always sending out data to controller
    #therefore sckl is out
    GPIO.setup(scdioPin, GPIO.OUT)
    #it has to sent 8 bits, starting with 0 for read
    # followed by adr that is read
    for i in range(8):
        #give the clock signal
        GPIO.output(scklPin, GPIO.LOW)
        #give first adr. bit
        GPIO.output(scdioPin, adr[i])
        #set up clock high to signal end of bit
        GPIO.output(scklPin, GPIO.HIGH)
    #now comes the reading of incoming data
    # therefor scdioPin is In
    GPIO.cleanup(scdioPin)
    GPIO.setup(scdioPin, GPIO.IN)
    #wait a mil.sec
    time.sleep(0.001)
    #here comes the data
    for i in range(8):
        #put clock low, to signal start
        GPIO.output(scklPin, GPIO.LOW)
        #set up clock high to signal end of bit
        GPIO.output(scklPin, GPIO.HIGH)
        #save data
        data.append(GPIO.input(scdioPin))
        
        #this cant be done to fast
        time.sleep(0.001)
    
    #return data byte
    return data

# data sents data to mouse-sensor
# input is: 1.adr list, 2. data list
# both lists have to have 8 bits each, first bit of adr. has to be 1
# this signals a writing op. to the controller
def writeData(adr,data):
    #sync pi and controller
    resync()
    #First act is always sending out data to controller
    #therefore sckl is out
    GPIO.setup(scdioPin, GPIO.OUT)
    #for loop to make adr clear (1 byte is always adr)
    for i in range(8):
        #give the clock signal
        GPIO.output(scklPin, GPIO.LOW)
        #give first adr. bit
        GPIO.output(scdioPin, adr[i])
        #set up clock high to signal end of bit
        GPIO.output(scklPin, GPIO.HIGH)
    
    #second loop to sent data
    for i in range(8):
        #give the clock signal
        GPIO.output(scklPin, GPIO.LOW)
        #give first data bit
        GPIO.output(scdioPin, data[i])
        #set up clock high to signal end of bit
        GPIO.output(scklPin, GPIO.HIGH)

#config can reset, power down or force awake the sensor
#here the pi can read and write, this is showen with first arg of func
# rw = TRUE means write, FALSE means read
#reset: 1000000
# power down: 01000000
# force awake: 00000001

def CONFIG_MOUSE(rw,data):
    #first check if read or write
    if rw:
        return writeData([0,0,0,0,0,0,0,0],data)
    else:
        return readData([0,0,0,0,0,0,0,0])


#status gives back the productID and Mouse State (aktiv, sleep)
#is at adr 0x01
#the ID is Bit 5,6,7 and awake is shown in bit 0
def STATUS():
    return readData([0,0,0,0,0,0,0,1])

#this function returns the dx value of the sensor
#the dx value is safed in adr. 0x03. this means the adr is 
# 00000011
# it is located as follows: 0 means 0 diff in x. +1 in motion is shown as
# 0x00 + 0x01. and +2 as 0x00 + 0x02
# -1 is shown as 0xFF, -2 as 0xFE
# the range is + 127 and -128
def dy():
    return readData([0,0,0,0,0,0,1,1])

#this function returns the dx value of the sensor
#the dx value is safed in adr. 0x02. this means the adr is 
# 00000010
# from Manual:  Y movement is counted since last report. Absolute value is determined by resolution. Reading clears the register
def dx():
    return readData([0,0,0,0,0,0,1,0])

#Squal returns the measure of the number of features visible by the sens
# see documentation of adns 2610 for more information
# it has adr. 0x04 = 00000100
def SQUAL():
    return readData([0,0,0,0,0,1,0,0])

# functions not implementet here: 
# Max_PIX at 0x05 and Min_PIX at 0x06
# Pixel_Sum at 0x07 and Actual pixel of surface at 0x08
# Shutter Upper (0x09) and Shutter Lower (0x0A)
# inv ProductID at 0x11

# data from readData is returned as a list of binary readings
# this function takes this list and returns a signed int
# movement in x/y can be from -128 to 127 (see comment in dx())
# so -5 means 5 steps in negativ direction
def fromSensToINT(data):
    #var to save in data
    temp = 0
    #transform from binary list to int
    for i in range(8):
        if data[i] ==0:
            temp = str(temp) + str(data[i])
        else:
            temp = str(temp) + str(data[i])
    #change temp from binary to int
    temp=int(temp,2)
    # give credit to signed int
    if temp > 127:
        temp = -255 + temp
        
    return temp

#driver code for testing
# adds up movments to have absolute value at the end of the for-loop
#addUpMovmentx = 0
#addUpMovmenty = 0
#set to zero

#dx()
#dy()
#for i in range(500):
    #addUpMovmentx += fromSensToINT(dx())
    #addUpMovmenty += fromSensToINT(dy())
    #print(addUpMovmentx, addUpMovmenty)
    #print(fromSensToINT(dx()))
    #time.sleep(0.00005)


