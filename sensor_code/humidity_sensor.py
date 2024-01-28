import RPi.GPIO as GPIO
import time

HUMIDITY_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(HUMIDITY_PIN, GPIO.IN)

def read_humidity_sensor():
    humidity_value = GPIO.input(HUMIDITY_PIN)
    return humidity_value

# humidity_value = read_humidity_sensor()
# print(f"Humidity Sensor Value: {humidity_value}")