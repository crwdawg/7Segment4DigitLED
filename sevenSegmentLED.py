#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep,time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
__author__ = 'Bill Curtis'
__credits__= 'https://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python'
__version__ = '1.0.0'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"
__status__ = "Production"

class fourDigitLED:
    """
    Driver to operate a common 7 segment 4 digit LED scrren with decimal points.
    This code assumes common annode LEDs which means that 0 turns the led on and 1 turns the led off.
    Each Pin can be changed when initializing the class.  The pins that I used are the defaults.
    Using this class is just as simple as initilizing the class and calling it with a number and a delay. delay defaults to 2 seconds    
        from eightSegmentLED import fourDigitLED
        LED = fourDigitLED     #this uses the default pins
        LED.display(88.88,5)   #this puts 88.88 on the display for 5 seconds
    """
    def __init__(self, pin1=24, pin2=25,pin3=12,pin4=16,pin5=20,pin6=21,pin7=22,pin8=5,pin9=6,pin10=13,pin11=19,pin12=26):
        self.pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10, pin11, pin12]       #all Pins for initilization
        self.segments = [pin1, pin2, pin3, pin4, pin5, pin7, pin10, pin11]               #Pins for LEDs in the segment
        self.digits = [pin12,pin9, pin8, pin6]                                           #pins that turn on/off the digit
        for pin in self.pins:                                                            #_initialize all digits off 
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,0)
            
    def _initialize(self):
        self._normalize()
        self._loadMatrix()

    def _normalize(self):
        self.number = str(self.number)
        try:
            if self.number.index('.') == '1':                                            #error correcting for float to string leading 0
                self.number = str(self.number).lstrip('0')
            elif self.number.index('.') == '4':                                          #error correcting for float to string trailing 0
                self.number = str(self.number).rstrip('0')
        except ValueError:
            pass
        self.number = self.number.rjust(5)
        try:
            self.decimal = self.number.index('.') -1                                      #save the place of the decimal index starts at 0
            self.number = self.number.replace('.','').rjust(4)                            #remove decimal
        except ValueError:
            self.decimal=3
            self.number = self.number.replace(' ','').rjust(4)
        if self.decimal < 0:                                                              #no decimal before four digit number
            self.number = ' err'
            self.decimal = 0
            print("decimal point cannot be before 1st digit")
        elif len(self.number) > 4:
            self.number = ' err'
            self.decimal = 3
            print("Number cannot have more than 4 digits")

    def _loadMatrix(self):                                                                #load digit representations into list
        self.digit: list = []
        self.matrix: list = []
        x = 0
        for x in (self.number):
            self.digit.append(x)
            self.matrix.append(self._getMatrix(x))
        self.matrix[self.decimal][2]=0                                                    #replaces decimal point
        return self.matrix

    def _getMatrix(self,num):                                                             #common anode uses 1 for off and 0 for on
        self.num = num
        num = {' ':[1,1,1,1,1,1,1,1],
        '0':[0,0,1,0,1,0,0,0],
        '1':[1,1,1,0,1,0,1,1],
        '2':[0,0,1,1,0,0,1,0],
        '3':[1,0,1,0,0,0,1,0],
        '4':[1,1,1,0,0,0,0,1],
        '5':[1,0,1,0,0,1,0,0],
        '6':[0,0,1,0,0,1,0,0],
        '7':[1,1,1,0,1,0,1,0],
        '8':[0,0,1,0,0,0,0,0],
        '9':[1,0,1,0,0,0,0,0],
        'e':[0,0,1,1,0,1,0,0],
        'r':[0,1,1,1,0,1,1,1]}
        id=num.get(self.num)
        return id

    def _loadIt(self):                                                                    #load the number into the LED
        m = self.matrix[self.loop]
        for y in range(0,8):
            GPIO.output(self.segments[y],m[y])

    def _flashIt(self):                                                                   #multiplex through the 4 digits
        for x in range(0,4):
            self.loop = x
            self._loadIt()
            GPIO.output(int(self.digits[x]),1)
            sleep(.0009)
            GPIO.output(int(self.digits[x]),0)

    def display(self,number,displayTime=2):                                               #this is the function to call for output
        self.number = number
        self.displayTime = int(displayTime)
        self._initialize()
        self._holdIt()

    def _holdIt(self):                                                                    #this sets how many seconds to hold the number
        try:
            now = time()
            then = now + self.displayTime
            while now < then:
                now = time()
                self._flashIt()
        except KeyboardInterrupt:
            print("Ctrl-c pressed")
            GPIO.cleanup()
