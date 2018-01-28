#!/usr/bin/python
#--------------------------------------
#  Rasbperry Pi ibutton with LCD Test Script
#
# Author : BehindTheSciences
# Date   : 15/02/2017
#
# http://behindthesciences.com
#
#--------------------------------------
import os
import time
import RPi.GPIO as GPIO
# Commands
LCD_CLEARDISPLAY        = 0x01
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_FUNCTIONSET         = 0x20
LCD_SETDDRAMADDR        = 0x80
# Entry flags
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTDECREMENT = 0x00
# Control flags
LCD_DISPLAYON           = 0x04
LCD_CURSOROFF           = 0x00
LCD_BLINKOFF            = 0x00
# Function set flags
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x8DOTS             = 0x00
# Offset for up to 4 rows.
LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

# GPIO to LCD mapping
LCD_RS            = 14
LCD_EN            = 18
LCD_D4            = 24
LCD_D5            = 23
LCD_D6            = 8
LCD_D7            = 25
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = LCD_SETDDRAMADDR # LCD RAM address for the 1st line
LCD_LINE_2 = LCD_SETDDRAMADDR | LCD_ROW_OFFSETS[1] # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
print(time.strftime("%c"))
 
os.system('modprobe wire timeout=1 slave_ttl=5')
os.system('modprobe w1-gpio')
os.system('modprobe w1-smem')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_slaves')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_remove')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_search')
base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
  
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_EN, GPIO.OUT)  # EN
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
  # Initialise display
  lcd_init()
 
  while True:
 
    # iButton Read
	f = open(base_dir, "r")
	ID = f.read()
	f.close()
	if ID != 'not found.\n':
		print(ID)
		lcd_string("iButton ID = ",LCD_LINE_1)
		lcd_string(ID,LCD_LINE_2)
		time.sleep(3)
		d = open(delete_dir, "w")
		d.write(ID)
	else:
		lcd_string("Waiting...",LCD_LINE_1)
		lcd_string(time.strftime("%c"),LCD_LINE_2)
    
	
 
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  # 000110 Cursor move direction
  lcd_byte(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT,LCD_CMD) 
  # Initialize display control, function, and mode registers.
  # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF,LCD_CMD)
  # 101000 Data length, number of lines, font size
  lcd_byte(LCD_FUNCTIONSET | LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS,LCD_CMD) # 101000 Data length, number of lines, font size
  # 000001 Clear display
  lcd_byte(LCD_CLEARDISPLAY,LCD_CMD) 
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_EN, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_EN, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()