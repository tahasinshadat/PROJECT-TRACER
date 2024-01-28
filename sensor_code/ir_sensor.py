import RPi.GPIO as GPIO
import time

IR_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

def read_ir_sensor():
    ir_value = GPIO.input(IR_PIN)
    return ir_value

# ir_value = read_ir_sensor()
# print(f"IR Sensor Value: {ir_value}")