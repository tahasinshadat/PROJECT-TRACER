from pitop.pma import UltrasonicSensor
import RPi.GPIO as GPIO
from movement_math import get_DC_from_angle
import time

GPIO.cleanup() # cleanup in case it did not run last time

def setup_motor(left:int, right:int, frequency):
    """Sets up motor given left and right pin
       Returns (Left GPIO PWM pin, right GPIO PWM pin)"""
    GPIO.setup(left, GPIO.OUT)
    GPIO.setup(right, GPIO.OUT)
    left_pwm = GPIO.PWM(left, frequency)
    right_pwm = GPIO.PWM(right, frequency)

    left_pwm.start(0)
    right_pwm.start(0)
    return (left_pwm, right_pwm)

def clockwise(left : GPIO.PWM, right: GPIO.PWM, speed):
    left.ChangeDutyCycle(speed)
    right.ChangeDutyCycle(0)

def counter_clockwise(left : GPIO.PWM, right: GPIO.PWM, speed):
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(speed)

def brakeMotor(left : GPIO.PWM, right: GPIO.PWM):
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)

motor_left_pin, motor_right_pin = 19, 26
servo_pin = 15

freq = 1000

motor_left, motor_right = setup_motor(motor_left_pin, motor_right_pin)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, 50)

def main():
    GPIO.setmode(GPIO.BCM)

    # SERVO
    print("Starting servo")
    servo.start(get_DC_from_angle(0))
    time.sleep(1)

    print("Straight")
    servo.ChangeDutyCycle(get_DC_from_angle(0))
    time.sleep(1)

    print("45 degrees CCW")
    servo.ChangeDutyCycle(get_DC_from_angle(45))
    time.sleep(1)

    print("Straight")
    servo.ChangeDutyCycle(get_DC_from_angle(0))
    time.sleep(1)

    print("45 CW")
    servo.ChangeDutyCycle(get_DC_from_angle(-45))
    time.sleep(1)

    print("Straight")
    servo.ChangeDutyCycle(get_DC_from_angle(0))
    time.sleep(1)

    # MOTOR
    print("Motor CW")
    clockwise(motor_left, motor_right, 25)
    time.sleep(1)

    print("Motor brake")
    brakeMotor(motor_left, motor_right)
    time.sleep(1)

    print("Motor CCW")
    counter_clockwise(motor_left, motor_right, 25)
    
    print("Motor brake")
    brakeMotor(motor_left, motor_right)
    time.sleep(1)

    GPIO.cleanup()

if __name__ == "__main__":
    main()