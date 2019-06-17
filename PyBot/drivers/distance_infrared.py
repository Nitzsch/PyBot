"""
This file is for the IR -Sensors. It uses the Adafruit_ADS1x15 script as a base. 
The Sensors are connected to a ADC from a generic chinese com., but it works alright with the Adafruit stuff
It is a 1015 (cheaper then the 1115 and does it stuff)

Usage:
call distance_channels("left" or "right")
returns a distance of the sensor

"""

import time
import Adafruit_ADS1x15
import pin_belegung as pin

channel_infrared_left = pin.get_infrared_left()
channel_infrared_right = pin.get_infrared_right()

#create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# read voltage values from channel via adc
def read_distance(channel):
    #start listening to channel on ADC
    adc.start_adc(channel, gain=GAIN)
    #one shot
    distance = adc.get_last_result()
    adc.stop_adc()

    return distance

#distance is measured by the infrared sensor in changes of Voltage.
#This needs to be converted into cm. 
# data to convert is taken out of the datasheet.
#IMPORTANT! 
#PLEASE NOTE: Voltage is a flipped x^2! it is low at all distances under 10cm
#peaks a high at 10cm (2.7V) and after that it gets low again. So this function does not 
# work correct if the distance is lower than 10cm or over 80cm.
def distance_channels(direction):
    if direction == "left":
        distance = read_distance(channel_infrared_left)
    else:
        distance = read_distance(channel_infrared_right)

    #the adc gives out numbers between 128-3300 out of adc datasheet
    #the channel input is div by 10 subtr. with 3. this is out of datasheet
    #endvalue is 20 to high (self-tested)
    #approximates value up to +/-2cm
    d = (516887 /(distance+ 3961)) -12
    return d

