#!/usr/bin/python
#--------------------------------------
#  16x2 LCD Rasbperry Pi Test Script
#
# Author : BehindTheSciences
# Date   : 14/02/2017
#
# https://behindthesciences.com
#
#--------------------------------------

import time

#LCD Commands
LCD_CLEARDISPLAY        = 0x01
LCD_RETURNHOME          = 0x02
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_CURSORSHIFT         = 0x10
LCD_FUNCTIONSET         = 0x20
LCD_SETCGRAMADDR        = 0x40
LCD_SETDDRAMADDR        = 0x80
# Entry flags
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
# Control flags
LCD_DISPLAYON           = 0x04
LCD_DISPLAYOFF          = 0x00
LCD_CURSORON            = 0x02
LCD_CURSOROFF           = 0x00
LCD_BLINKON             = 0x01
LCD_BLINKOFF            = 0x00
# Move flags
LCD_DISPLAYMOVE         = 0x08
LCD_CURSORMOVE          = 0x00
LCD_MOVERIGHT           = 0x04
LCD_MOVELEFT            = 0x00
# Function set flags
LCD_8BITMODE            = 0x10
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x10DOTS            = 0x04
LCD_5x8DOTS             = 0x00

# Offset for up to 4 rows.
LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = LCD_SETDDRAMADDR # LCD RAM address for the 1st line
LCD_LINE_2 = LCD_SETDDRAMADDR | LCD_ROW_OFFSETS[1] # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class BTSLCD():
 
    def __init__(self, gpio,lcd_en,lcd_rs,lcd_d4,lcd_d5,lcd_d6,lcd_d7):
      # Initialise 
      self._gpio = gpio
      self._lcd_en = lcd_en
      self._lcd_rs = lcd_rs
      self._lcd_d4 = lcd_d4
      self._lcd_d5 = lcd_d5
      self._lcd_d6 = lcd_d6
      self._lcd_d7 = lcd_d7

     
    def lcd_init(self):
      #initialise GPIO
      self._gpio.setup(self._lcd_en, self._gpio.OUT)  # EN
      self._gpio.setup(self._lcd_rs, self._gpio.OUT) # RS
      self._gpio.setup(self._lcd_d4, self._gpio.OUT) # DB4
      self._gpio.setup(self._lcd_d5, self._gpio.OUT) # DB5
      self._gpio.setup(self._lcd_d6, self._gpio.OUT) # DB6
      self._gpio.setup(self._lcd_d7, self._gpio.OUT) # DB7
      # Initialise display
      self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
      # 000110 Cursor move direction
      self.lcd_byte(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT,LCD_CMD) 
      # Initialize display control, function, and mode registers.
      # 001100 Display On,Cursor Off, Blink Off
      self.lcd_byte(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF,LCD_CMD)
      # 101000 Data length, number of lines, font size
      self.lcd_byte(LCD_FUNCTIONSET | LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS,LCD_CMD) # 101000 Data length, number of lines, font size
      # 000001 Clear display
      self.lcd_byte(LCD_CLEARDISPLAY,LCD_CMD) 
      time.sleep(E_DELAY)
     
    def lcd_byte(self,bits, mode):
      # Send byte to data pins
      # bits = data
      # mode = True  for character
      #        False for command
     
      self._gpio.output(self._lcd_rs, mode) # RS
     
      # High bits
      self._gpio.output(self._lcd_d4, False)
      self._gpio.output(self._lcd_d5, False)
      self._gpio.output(self._lcd_d6, False)
      self._gpio.output(self._lcd_d7, False)
      if bits&0x10==0x10:
        self._gpio.output(self._lcd_d4, True)
      if bits&0x20==0x20:
        self._gpio.output(self._lcd_d5, True)
      if bits&0x40==0x40:
        self._gpio.output(self._lcd_d6, True)
      if bits&0x80==0x80:
        self._gpio.output(self._lcd_d7, True)
     
      # Toggle 'Enable' pin
      self.lcd_toggle_enable()
     
      # Low bits
      self._gpio.output(self._lcd_d4, False)
      self._gpio.output(self._lcd_d5, False)
      self._gpio.output(self._lcd_d6, False)
      self._gpio.output(self._lcd_d7, False)
      if bits&0x01==0x01:
        self._gpio.output(self._lcd_d4, True)
      if bits&0x02==0x02:
        self._gpio.output(self._lcd_d5, True)
      if bits&0x04==0x04:
        self._gpio.output(self._lcd_d6, True)
      if bits&0x08==0x08:
        self._gpio.output(self._lcd_d7, True)
     
      # Toggle 'Enable' pin
      self.lcd_toggle_enable()
     
    def lcd_toggle_enable(self):
      # Toggle enable
      time.sleep(E_DELAY)
      self._gpio.output(self._lcd_en, True)
      time.sleep(E_PULSE)
      self._gpio.output(self._lcd_en, False)
      time.sleep(E_DELAY)
     
    def lcd_string(self,message,line):
      # Send string to display
     
      message = message.ljust(LCD_WIDTH," ")
      if line == 1:
	P_Line = LCD_LINE_1
      else:
	P_Line = LCD_LINE_2

      self.lcd_byte(P_Line, LCD_CMD)
     
      for i in range(LCD_WIDTH):
        self.lcd_byte(ord(message[i]),LCD_CHR)
