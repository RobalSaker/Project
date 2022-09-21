#code Robal Saker for IOT project
import pycom
import _thread
from network import WLAN
import machine # Interfaces with hardware components
from machine import Pin # Pin object to configure pins
from machine import ADC # ADC object to configure reading values
import time  # Allows use of time.sleep() for delays
from dht import DHT

#MQTT callback
def sub_cb(topic, msg):
   print(msg)
print("Welcome to the Greenhouse Monitoring System v1.1")


soil_moisture_pin = 'P18' # sensor is connected to anologe output of soil moisture sensor.
coil_pin = Pin(soil_moisture_pin, mode=Pin.IN)  # set up soil moisture sensor pin mode to input
adc = ADC()
coil_read = adc.channel(pin=soil_moisture_pin, attn=ADC.ATTN_11DB) #save soil_moisture reading values

temp_pin = adc.channel(pin='P20') # Analog indoor temperature sensor pin

Plant_Light=Pin('P4', Pin.OUT, pull = Pin.PULL_DOWN) # initialize `P4` in gpio mode and make it an output and  PULL_DOWN enabled to control Plant_Light in dark.

def LDR(): #photoresistor passive component that decreases resistance with respect to receiving luminosity.
 LDRSensorPin = 'P16'
 lightPin = Pin(LDRSensorPin, mode=Pin.IN)
 #adc = ADC(bits=10)             # create an ADC object bits=10 means range 0-1024 the lower value the less light detected
 LDR_pin = adc.channel(attn=ADC.ATTN_11DB, pin=LDRSensorPin)
 LDR_value = LDR_pin() # read an analog value
 #print("plantlight :", LDR_value)
 # if LDR value higher than 1000 then switch the Plant_Light on
 if(LDR_value>1000):
     Plant_Light.value(1) #plantlight on
 else:
     Plant_Light.value(0) #plantlight off
 return  LDR_value


redLed=Pin('P10', Pin.OUT, pull = Pin.PULL_DOWN) #initialize `P10` in gpio mode and make it an output and  PULL_DOWN enabled Red Led for temperature
yalloLed=Pin('P9', Pin.OUT, pull = Pin.PULL_DOWN) #initialize `P9` in gpio mode and make it an output and  PULL_DOWN enabled Yallow led fot temperature
greenLed=Pin('P8', Pin.OUT, pull = Pin.PULL_DOWN) #initialize `P8` in gpio mode and make it an output and  PULL_DOWN enabled Green led for temperature

th = DHT(Pin('P2', mode=Pin.OPEN_DRAIN), 0)


while True:
    millivolts = temp_pin.voltage() # Analog temperature measured in millivolts
    degC = (millivolts - 500.0) / 10.0 # Convert millivolts to celsius
    soil_moisture = coil_read.value() #recall for soil_moisture values
    result = th.read()
    pybytes.send_signal(20, str(degC)) #send temperature value to pybytes
    pybytes.send_signal(18, soil_moisture) #send soil_moisture value to pybytes
    pybytes.send_signal(16, str(LDR())) #send LDR value to pybytes
    pybytes.send_signal(4, result.humidity)

    print('Temp:', result.temperature)
    print('RH:', result.humidity)
    print("LDR ", str(LDR()))
    print("Temp_value ", str(degC))
    print("coil value: ",soil_moisture)


    time.sleep(10) # put the program in sleep for n second
    # If temperature is higher than 28 degrees celsius
    if(degC >= 28):
        redLed.value(1)
        greenLed.value(0)
        yalloLed.value(0)

    elif(degC <28 and degC >22):
        redLed.value(0)
        greenLed.value(0)
        yalloLed.value(1)

    else:
        redLed.value(0)
        greenLed.value(1)
        yalloLed.value(0)
