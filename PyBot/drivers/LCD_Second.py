#!/usr/bin/python
# https://tutorials-raspberrypi.de/raspberry-pi-lcd-display-16x2-hd44780/
#Usage:
#LCD needs to be init() first use
# after that the msg is send like:
#    lcd_send_byte(1, "H")
#    lcd_message("Hello")
#    lcd_send_byte(2, "H")
#    lcd_message("World!")

import time
#import RPi.GPIO as GPIO
import mcp23017 as GPIO
import pin_belegung as pins


lcd_pins = pins.get_LCD()

# Pin configs
LCD_RS = lcd_pins[0]
LCD_E  = lcd_pins[1]
LCD_DATA4 = lcd_pins[2]
LCD_DATA5 = lcd_pins[3]
LCD_DATA6 = lcd_pins[4]
LCD_DATA7 = lcd_pins[5]

LCD_WIDTH = 16      # Zeichen je Zeile
LCD_LINE_1 = 0x80   # Adresse der ersten Display Zeile
LCD_LINE_2 = 0xC0   # Adresse der zweiten Display Zeile
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005

# turns string message from message function to bytes
# is used for lcd display of text
def lcd_send_byte(bits, mode):
    # Pins auf LOW setzen
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)
    if bits & 0x10 == 0x10:
      GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits & 0x20 == 0x20:
      GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits & 0x40 == 0x40:
      GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits & 0x80 == 0x80:
      GPIO.output(LCD_DATA7, GPIO.HIGH)
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, GPIO.HIGH)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)  
    time.sleep(E_DELAY)      
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)
    if bits&0x01==0x01:
      GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits&0x02==0x02:
      GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits&0x04==0x04:
      GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits&0x08==0x08:
      GPIO.output(LCD_DATA7, GPIO.HIGH)
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, GPIO.HIGH)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)  
    time.sleep(E_DELAY)  
    
#init the lcd display with blanks

def display_init():
    lcd_send_byte(0x33, LCD_CMD)
    lcd_send_byte(0x32, LCD_CMD)
    lcd_send_byte(0x28, LCD_CMD)
    lcd_send_byte(0x0C, LCD_CMD)  
    lcd_send_byte(0x06, LCD_CMD)
    lcd_send_byte(0x01, LCD_CMD)  

#sents message to lcd 
def lcd_message(message):
    message = message.ljust(LCD_WIDTH," ")  
    for i in range(LCD_WIDTH):
      lcd_send_byte(ord(message[i]),LCD_CHR)
		
GPIO.start(0x20)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_DATA4, GPIO.OUT)
GPIO.setup(LCD_DATA5, GPIO.OUT)
GPIO.setup(LCD_DATA6, GPIO.OUT)
GPIO.setup(LCD_DATA7, GPIO.OUT)

display_init()

lcd_send_byte(LCD_LINE_1, LCD_CMD)
lcd_message("Es scheint zu")
lcd_send_byte(LCD_LINE_2, LCD_CMD)
lcd_message("funktionieren :)")
