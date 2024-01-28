import RPi.GPIO as GPIO
import time

GAS_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(GAS_PIN, GPIO.IN)

def read_gas_sensor():
    gas_value = GPIO.input(GAS_PIN)
    return gas_value

# gas_value = read_gas_sensor()
# print(f"Gas Sensor Value: {gas_value}")