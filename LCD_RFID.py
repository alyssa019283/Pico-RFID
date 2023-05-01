from machine import Pin
from mfrc522 import MFRC522
import utime
 
reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)

buzzer = machine.PWM(Pin(27))
correct_sound = [2637, 2637, 2637, 2637, 0, 0]
wrong_sound = [1500, 1500, 850, 850, 850, 0, 0]

red = Pin(0, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)

rs = Pin(16, Pin.OUT)
e = Pin(17, Pin.OUT)
d4 = Pin(18, Pin.OUT)
d5 = Pin(19, Pin.OUT)
d6 = Pin(20, Pin.OUT)
d7 = Pin(21, Pin.OUT)

print("Place RFID tag on the reader:")
print("")

def sound(frequencies):
    for i in frequencies:
        if i == 0:
            buzzer.duty_u16(0)            
        else:
            buzzer.freq(i)                
            buzzer.duty_u16(19660)        
        utime.sleep(0.20) 
 
def pulseE():
    e.value(1)
    utime.sleep_us(40)
    e.value(0)
    utime.sleep_us(40)
    
def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
    
def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >>4)
    d5.value((BinNum & 0b00100000) >>5)
    d6.value((BinNum & 0b01000000) >>6)
    d7.value((BinNum & 0b10000000) >>7)
    pulseE()
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
    
def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)                   #8 bit
    send2LCD4(0b0011)					#8 bit
    send2LCD4(0b0011)					#8 bit
    send2LCD4(0b0010)					#4 bit
    send2LCD8(0b00101000)				#4 bit,2 lines?,5*8 bots
    send2LCD8(0b00001100)				#lcd on, blink off, cursor off.
    send2LCD8(0b00000110)				#increment cursor, no display shift
    send2LCD8(0b00000001)				#clear screen
    utime.sleep_ms(2)					#clear screen needs a long delay
 
setUpLCD()
rs.value(1)
for x in "Welcome!":
    send2LCD8(ord(x))
        
 
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        card = int.from_bytes(bytes(uid),"little",False)
            
        if card == 2726286576:
            print("Card ID: " + str(card) + " ACCESS GRANTED")
            red.value(0)
            green.value(1)
            blue.value(0)
            sound(correct_sound)
            
            setUpLCD()
            rs.value(1)
            for x in "Access Granted":
                send2LCD8(ord(x))
                    
        else:
            print("Card ID: " + str(card) + " ACCESS DENIED")
            red.value(1)
            green.value(0)
            blue.value(0)
            sound(wrong_sound)
            
            setUpLCD()
            rs.value(1)
            for x in "Access Denied":
                send2LCD8(ord(x))
