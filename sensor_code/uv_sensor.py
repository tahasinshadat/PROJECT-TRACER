import RPi.GPIO as GPIO
import time

UV_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(UV_PIN, GPIO.IN)

def read_uv_sensor():
    uv_value = GPIO.input(UV_PIN)
    return uv_value

# uv_value = read_uv_sensor()
# print(f"UV Sensor Value: {uv_value}")