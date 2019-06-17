#!/usr/bin/python

# Idea:
# https://tutorials-raspberrypi.de/raspberry-pi-lcd-display-16x2-hd44780/


# Usage:
# import this file.
# sent msg with write_lcd(line, msg)
# line can be 1 or 2, msg is a string
# max string length is given from display: 16 Bits

import time
import mcp23017 as mcp
#import sensors.pin_belegung as pins

#lcd_pins = pins.get_LCD()
# [lcd_rs, lcd_e, lcd_d4, lcd_d5, lcd_d6, lcd_d7]
# Pin configs
LCD_RS = 14 #lcd_pins[0]
LCD_E = 13 #lcd_pins[1]
LCD_DATA4 = 12 #lcd_pins[2]
LCD_DATA5 = 11#lcd_pins[3]
LCD_DATA6 = 10 #lcd_pins[4]
LCD_DATA7 = 9 #lcd_pins[5]


LCD_WIDTH = 16  # Zeichen je Zeile
LCD_LINE_1 = 0x80  # Adresse LCD Zeile 1
LCD_LINE_2 = 0xC0  # Adresse LCD Zeile 2
LCD_CHR = mcp.HIGH
LCD_CMD = mcp.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005


def display_init():
    lcd_write_byte(0x33, LCD_CMD)
    lcd_write_byte(0x32, LCD_CMD)
    lcd_write_byte(0x28, LCD_CMD)
    lcd_write_byte(0x0C, LCD_CMD)
    lcd_write_byte(0x06, LCD_CMD)
    lcd_write_byte(0x01, LCD_CMD)


def lcd_write_byte(bits, mode):
    # Pins auf LOW setzen
    mcp.output(LCD_RS, mode)
    mcp.output(LCD_DATA4, mcp.LOW)
    mcp.output(LCD_DATA5, mcp.LOW)
    mcp.output(LCD_DATA6, mcp.LOW)
    mcp.output(LCD_DATA7, mcp.LOW)
    if bits & 0x10 == 0x10:
        mcp.output(LCD_DATA4, mcp.HIGH)
    if bits & 0x20 == 0x20:
        mcp.output(LCD_DATA5, mcp.HIGH)
    if bits & 0x40 == 0x40:
        mcp.output(LCD_DATA6, mcp.HIGH)
    if bits & 0x80 == 0x80:
        mcp.output(LCD_DATA7, mcp.HIGH)
    time.sleep(E_DELAY)
    mcp.output(LCD_E, mcp.HIGH)
    time.sleep(E_PULSE)
    mcp.output(LCD_E, mcp.LOW)
    time.sleep(E_DELAY)
    mcp.output(LCD_DATA4, mcp.LOW)
    mcp.output(LCD_DATA5, mcp.LOW)
    mcp.output(LCD_DATA6, mcp.LOW)
    mcp.output(LCD_DATA7, mcp.LOW)
    if bits & 0x01 == 0x01:
        mcp.output(LCD_DATA4, mcp.HIGH)
    if bits & 0x02 == 0x02:
        mcp.output(LCD_DATA5, mcp.HIGH)
    if bits & 0x04 == 0x04:
        mcp.output(LCD_DATA6, mcp.HIGH)
    if bits & 0x08 == 0x08:
        mcp.output(LCD_DATA7, mcp.HIGH)
    time.sleep(E_DELAY)
    mcp.output(LCD_E, mcp.HIGH)
    time.sleep(E_PULSE)
    mcp.output(LCD_E, mcp.LOW)
    time.sleep(E_DELAY)


def lcd_message(message):
    message = message.ljust(LCD_WIDTH, " ")
    for i in range(LCD_WIDTH):
        lcd_write_byte(ord(message[i]), LCD_CHR)


def write_lcd(line=1, msg="MSG failure"):
    if line ==1:
        lcd_write_byte(LCD_LINE_1, LCD_CMD)
        lcd_message(msg)
    else:
        lcd_write_byte(LCD_LINE_2, LCD_CMD)
        lcd_message(msg)

#Init
mcp.start(0x20)
mcp.setup(LCD_E, mcp.OUT)
mcp.setup(LCD_RS, mcp.OUT)
mcp.setup(LCD_DATA4, mcp.OUT)
mcp.setup(LCD_DATA5, mcp.OUT)
mcp.setup(LCD_DATA6, mcp.OUT)
mcp.setup(LCD_DATA7, mcp.OUT)

display_init()

