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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from BTSLCDPi import BTSLCD

LCD_LINE_1 = 1
LCD_LINE_2 = 2

# GPIO to LCD mapping
LCD_RS            = 14
LCD_EN            = 18
LCD_D4            = 24
LCD_D5            = 23
LCD_D6            = 8
LCD_D7            = 25

print(time.strftime("%c"))
 
os.system('modprobe wire timeout=1 slave_ttl=5')
os.system('modprobe w1-gpio')
os.system('modprobe w1-smem')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_slaves')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_remove')
os.system('chmod a+w /sys/devices/w1_bus_master1/w1_master_search')
base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'

#Create LCD class
LCD = BTSLCD(GPIO,LCD_EN,LCD_RS,LCD_D4,LCD_D5,LCD_D6,LCD_D7)
  
def main():

 
  # Initialise display
  LCD.lcd_init()
 
  while True:
 
    # iButton Read
	f = open(base_dir, "r")
	ID = f.read()
	f.close()
	if ID != 'not found.\n':
		print(ID)
		LCD.lcd_string("iButton ID = ",LCD_LINE_1)
		LCD.lcd_string(ID,LCD_LINE_2)
		time.sleep(10)
		d = open(delete_dir, "w")
		d.write(ID)
	else:
		LCD.lcd_string("Waiting...",LCD_LINE_1)
		LCD.lcd_string(time.strftime("%c"),LCD_LINE_2)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
