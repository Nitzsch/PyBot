"""
This is a implementation of an accelorate-driver given with most generic chips on the marked. 
not done by myself. 
I just commented most of the stuff out, cause they made the start of this script real slow. At the init phase, 
this script runs 50 test reads to calibrate the sensor. We just need the yaw-angle. all the other stuff is a waste
for us. 

Usage:
just call yaw()
it returns the yaw-angle of that moment. Remember: it is given in DEG and the total value of a circle is (do not know why) 217...
"""

import smbus
import time

PWR_M   = 0x6B
DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47
TEMP = 0x41
bus = smbus.SMBus(1)

Device_Address = 0x68   # device address

#AxCal=0
#AyCal=0
#AzCal=0
#GxCal=0
GyCal=0
GzCal=0

def InitMPU():
     bus.write_byte_data(Device_Address, DIV, 7)
     bus.write_byte_data(Device_Address, PWR_M, 1)
     bus.write_byte_data(Device_Address, CONFIG, 0)
     bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
     bus.write_byte_data(Device_Address, INT_EN, 1)
     time.sleep(1)
     
def readMPU(addr):
     high = bus.read_byte_data(Device_Address, addr)
     low = bus.read_byte_data(Device_Address, addr+1)
     value = ((high << 8) | low)
     if(value > 32768):
           value = value - 65536
     return value
"""
def accel():
     x = readMPU(ACCEL_X)
     y = readMPU(ACCEL_Y)
     z = readMPU(ACCEL_Z)
     Ax = (x/16384.0-AxCal)
     Ay = (y/16384.0-AyCal)
     Az = (z/16384.0-AzCal)
     return [Ax,Ay,Az]
"""    
def gyro():
      #global GxCal
      global GyCal
      global GzCal
      #x = readMPU(GYRO_X)
      #y = readMPU(GYRO_Y)
      z = readMPU(GYRO_Z)
      #Gx = x/131.0 - GxCal
      #Gy = y/131.0 - GyCal
      #Gz = z/131.0 - GzCal
      #return [Gx,Gy,Gz]
      return z/131.0 - GyCal

def calibrate():

  #global AxCal
  #global AyCal
  #global AzCal
  #x=0
  #y=0
  #z=0
  #for i in range(50):
  #    x = x + readMPU(ACCEL_X)
  #    y = y + readMPU(ACCEL_Y)
  #    z = z + readMPU(ACCEL_Z)
  #x= x/50
  #y= y/50
  #z= z/50
  #AxCal = x/16384.0
  #AyCal = y/16384.0
  #AzCal = z/16384.0
  
  #global GxCal
  global GyCal
  global GzCal
  z=0
  
  y=0
  #x=0
  for i in range(50):
    #x = x + readMPU(GYRO_X)
    y = y + readMPU(GYRO_Y)
    z = z + readMPU(GYRO_Z)
  #x= x/50
  y= y/50
  z= z/50
  #GxCal = x/131.0
  GyCal = y/131.0
  GzCal = z/131.0

 
InitMPU()
calibrate()


def yaw():
  gy = gyro()
  if gy > 0.8 or gy < -0.8:
    return int(gy)
  else:
    return 0


