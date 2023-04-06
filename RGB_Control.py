from machine import Pin
from mfrc522 import MFRC522
from pitches import *
import utime
       
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

# Pin location for the in-built buzzer is 18 on the 'Maker Pi Pico' board
buzzer = machine.PWM(Pin(18))
# Using pulse width modulation to vary the frequency of sound
correct_sound = [2637, 2637, 2637, 2637, 0, 0]
wrong_sound = [1500, 1500, 850, 850, 850, 0, 0]

# Setting the location of the RGB pins
red = Pin(0, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)
 
print("Place RFID tag on the reader:")
print("")
 
def sound(frequencies):
    for i in frequencies:
                if i == 0:
                    buzzer.duty_u16(0)            # 0% duty cycle
                else:
                    buzzer.freq(i)                # Setting the frequency
                    buzzer.duty_u16(19660)        # 30% duty cycle
                utime.sleep(0.20) 

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        card = int.from_bytes(bytes(uid),"little",False)
        # Change UID value depending on your UID   
        if card == 2726286576:
            print("Card ID: " + str(card) + " ACCESS GRANTED")
            # Green light on
            red.value(0)
            green.value(1)
            blue.value(0)
            sound(correct_sound)                
        else:
            print("Card ID: " + str(card) + " ACCESS DENIED")
            # Red light on
            red.value(1)
            green.value(0)
            blue.value(0)
            sound(wrong_sound)
