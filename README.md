# Raspberry-Pi-ibutton
Python code to read ibuttons DS1990 with a Raspberry Pi
This code uses the 1-wire bus of the Raspberry Pi
For more info, please visit:
https://behindthesciences.com/electronics/raspberry-pi-ibutton-system/

## Display results on Terminal only
```ruby
sudo python ibutton.py
```
## Display ibutton ID on LCD
![LCD_Pi_Ibutton](https://github.com/BehindTheSciences/Raspberry-Pi-ibutton/blob/master/Raspberry-Pi-Ibutton-LCD-2.png)
##### LCD Raspberry Pi Connections

|LCD Pin|	Function |	Pi Pin |
|------|------|------|
|1|	GND|	GND|
|2|	+5V	|+5V|
|3|	Vo (Contrast)|	GND|
|4|	RS	|GPIO-14|
|5|	RW	|GND|
|6|	Enable|	GPIO-18|
|7|	D0	|Not in Use|
|8|	D1	|Not in Use|
|9|	D2	|Not in Use|
|10|	D3|	Not in Use|
|11	|D4	|GPIO-24|
|12	|D5	|GPIO-23|
|13|	D6|	GPIO-8|
|14	|D7	|GPIO-25|
|15|	+5V (Backlight)|	+5V|
|16	|GND(Backlight)|	GND|

##### Command
```ruby
sudo python ibuttonLCD.py
```
