import RPi.GPIO as GPIO
import time

# Pin configurations
potPin = 0
actuatorInPin1 = 17
actuatorInPin2 = 18

# Actuator stroke and ratio for conversion
stroke = 3.937
minStroke = 0.1
maxStroke = 3.84
strokeRatio = 1024 / stroke

def setup():
    # Initialize GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(potPin, GPIO.IN)
    GPIO.setup(actuatorInPin1, GPIO.OUT)
    GPIO.setup(actuatorInPin2, GPIO.OUT)
    GPIO.output(actuatorInPin1, GPIO.LOW)
    GPIO.output(actuatorInPin2, GPIO.LOW)

def motor_drive(mode):
    # Control the linear actuator movement
    if mode == 'r' or mode == 'R':
        GPIO.output(actuatorInPin1, GPIO.HIGH)
        GPIO.output(actuatorInPin2, GPIO.LOW)
    elif mode == 'f' or mode == 'F':
        GPIO.output(actuatorInPin1, GPIO.LOW)
        GPIO.output(actuatorInPin2, GPIO.HIGH)
    elif mode == 's' or mode == 'S':
        GPIO.output(actuatorInPin1, GPIO.LOW)
        GPIO.output(actuatorInPin2, GPIO.LOW)
    else:
        GPIO.output(actuatorInPin1, GPIO.LOW)
        GPIO.output(actuatorInPin2, GPIO.LOW)

def drive_arm_to_position(position):
    # Drive the linear actuator to the specified position
    if position > maxStroke or position < minStroke:
        motor_drive('s')
    else:
        distance_to_pot_val = convert_position_to_pot_value(position)
        if distance_to_pot_val > GPIO.input(potPin):
            motor_drive('f')
        elif distance_to_pot_val < GPIO.input(potPin):
            motor_drive('r')
        else:
            motor_drive('s')

def convert_position_to_pot_value(position):
    # Convert the desired position to potentiometer value
    return int(position * strokeRatio)

def time_test_motor():
    # Perform a time test for motor movement
    motor_drive('f')
    time.sleep(0.5)
    motor_drive('s')
    time.sleep(0.5)
    motor_drive('r')
    time.sleep(0.5)
    motor_drive('s')
    time.sleep(3)

def cleanup():
    # Clean up GPIO resources
    GPIO.cleanup()

def move_arm_to(position):
    # Move the arm to the specified position
    setup()
    drive_arm_to_position(position)
    cleanup()

move_arm_to(2.84)
