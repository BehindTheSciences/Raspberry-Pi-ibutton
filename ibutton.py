#!/usr/bin/python
#--------------------------------------
#  Rasbperry Pi ibutton Test Script
#
# Author : BehindTheSciences
# Date   : 15/02/2017
#
# https://behindthesciences.com
#
#--------------------------------------
import os
import time
import RPi.GPIO as GPIO
  
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

  while True:
  
    # iButton Read
    f = open(base_dir, "r")
    ID = f.read()
    f.close()
    if ID != 'not found.\n':
        print(ID)
        time.sleep(3)
        d = open(delete_dir, "w")
        d.write(ID)
    else:
        print("Waiting") 
  
if __name__ == '__main__':
  
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
