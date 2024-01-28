import RPi.GPIO as GPIO
import time

TEMP_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(TEMP_PIN, GPIO.IN)

def read_temp_sensor():
    temp_value = GPIO.input(TEMP_PIN)
    return temp_value

# temp_value = read_temp_sensor()
# print(f"Temperature Sensor Value: {temp_value}")