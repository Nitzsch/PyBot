"""
This file manages all the pins of the pi and the mcp23017. 

Remember: The pins are given in BOARD! 
IMPORTANT: BOARD!

import this file only in driver scripts. if you need it somewhere else you are doing something wrong. 

"""

# Diese Datei dient der organisation der Pinbelegung. 
# Es wird im ganzen Framework exakt einmal die Pinbelegung festgelegt und zwar hier
# und per funct nach dem Pin gefragt. Die Pins sind in GPIO.BOARD angegeben!

#I2C
pin_I2C_data = 2
pin_I2C_clock = 5

#Mouse_Sensor
mouse_sens_data = 33
mouse_sens_clk = 35

#LCD is mcp
lcd_rs = 14
lcd_e = 13
lcd_d4 = 12
lcd_d5 = 11
lcd_d6 = 10
lcd_d7 =9

#Motor
# motor1 = l293d.DC(22,18,16)
motor1_en= 40
motor1_in0= 38
motor1_in1= 36
# motor2 = l293d.DC(13,11,15)
motor2_en= 22
motor2_in0= 16
motor2_in1= 18

#Sonar-Dist
sonar_trig_r = 7
sonar_eccho_r = 11

sonar_trig_f = 13
sonar_eccho_f = 15

sonar_trig_l= 31
sonar_eccho_l = 29

#Buttons, stuff
start_button = 21

#ADC Pins
infrared_left = 3
infrared_right = 2
infrared_cliff = 1

#IF Sensors
wheel_left_sens = 32
wheel_right_sens = 23
#mcp
cliff_sens1 = 8 
cliff_sens2 = 7

def get_mouse_sensor():
    return [mouse_sens_data, mouse_sens_clk]

def get_LCD():
    return [lcd_rs, lcd_e, lcd_d4, lcd_d5, lcd_d6, lcd_d7]

def get_motor1():
    return [motor1_en, motor1_in0, motor1_in1]

def get_motor2():   
    return [motor2_en, motor2_in0, motor2_in1]

def get_sonar():
    return [sonar_trig_l, sonar_eccho_l, sonar_trig_f, sonar_eccho_f, sonar_trig_r, sonar_eccho_r]

def get_start_button():
    return start_button

def get_infrared_left():
    return infrared_left

def get_infrared_right():
    return infrared_right
    
def get_cliff_sens():
    return [cliff_sens1,cliff_sens2]
    
def get_wheel_encoder():
    return [wheel_left_sens,wheel_right_sens]
    
    
