#!/usr/bin/env python
from sevenSegmentLED import fourDigitLED

LED = fourDigitLED()
again = ''
number = ''
duration = ''  #demonstrating that the function will change the string to a number automatically
try:
    while again != 'n':
        number = input("What number would you like to display?  ")
        duration = input("How long would you like to display the number?  ")
        LED.display(number,duration)
        again = input("Do you want to display another number?  (n to quit)")
        

except KeyboardInterrupt:
    print("Ctrl-c pressed")