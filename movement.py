
from pitop.pma import UltrasonicSensor
import RPi.GPIO as GPIO
from time import sleep
import math

from movement_math import get_DC_from_angle

print("Setting up board")
GPIO.setmode(GPIO.BCM)
print("board set up")

#############
# Pin Setup #
#############

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

# MOTORS
# FRONT
FLL = 19
FLR = 26
FRL = 20
FRR = 21
# BACK
# BLL = 
# BLR =
# BRL =
# BRR =

frequency = 1000

left_white, left_red = setup_motor(FLL, FLR, frequency)
right_white, right_red = setup_motor(FRL, FRR, frequency)
left_white, left_red = setup_motor(FLL, FLR, frequency)
right_white, right_red = setup_motor(FRL, FRR, frequency)

# SERVO
FL = 3
FR = 14
BL = 4
BR = 15

FLServo = GPIO.PWM(FL, 50)
FRServo = GPIO.PWM(FR, 50)
BLServo = GPIO.PWM(BL, 50)
BRServo = GPIO.PWM(BR, 50)

FLServo.start(get_DC_from_angle(0))
FRServo.start(get_DC_from_angle(0))
BLServo.start(get_DC_from_angle(0))
BRServo.start(get_DC_from_angle(0))

print("Pins set up")

###################
# Motor Functions #
###################

def clockwise(left : GPIO.PWM, right: GPIO.PWM, speed):
    left.ChangeDutyCycle(speed)
    right.ChangeDutyCycle(0)

def counter_clockwise(left : GPIO.PWM, right: GPIO.PWM, speed):
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(speed)

def brakeMotor(left : GPIO.PWM, right: GPIO.PWM):
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)

def forward(left_speed, right_speed):
    clockwise(left_white, left_red, left_speed)
    clockwise(right_white, right_red, right_speed)

def backward(left_speed, right_speed):
    counter_clockwise(left_white, left_red, left_speed)
    counter_clockwise(right_white, right_red, right_speed)

def brake():
    brakeMotor(left_white, left_red)
    brakeMotor(right_white, right_red)

def turn_left_dime(speed):
    counter_clockwise(left_white, left_red, speed)
    clockwise(right_white, right_red, speed)

def turn_right_dime(speed):
    clockwise(left_white, left_red, speed)
    counter_clockwise(right_white, right_red, speed)

############
# commands #
############
    
def move_forward_amount(speed, time):
    forward(speed, speed)
    sleep(time)
    brake()

def move_backward_amount(speed, time):
    backward(speed, speed)
    sleep(time)
    brake()

###################
# Component Setup #
###################
    
side_front = UltrasonicSensor("D7")
side_back = UltrasonicSensor("D0")
front = UltrasonicSensor("D3")
# back = UltrasonicSensotr("")

side = 1 # 0 is back, 1 is forward

sensors = [side_front, side_back]

base_speed = 50

speeds = [base_speed, base_speed] # left, right

cycle = 0

previous_dist = sensors[side].distance

def auto_drive():
    try:
        print("Starting loop")
        while True:
            # stop
            if front.distance < .20:
                print("STOPPING: " + str(front.distance))
                brake()
                break
                # cycle += 1
                # if cycle == 2:
                #     break

                # target_dist = sensors[side].distance
                # side = (side + 1) % 2

                # if side == 0:
                #     turn = turn_left_dime
                # else:
                #     turn = turn_right_dime

                # while sensors[side].distance > target_dist:
                #     turn(base_speed)

            distance = sensors[side].distance
            print(distance)
            # in range correction
            if distance > previous_dist:
                speeds[side] = base_speed - 5
                speeds[side-1] = base_speed + 5
            if distance < previous_dist:
                speeds[side] = base_speed + 5
                speeds[side-1] = base_speed - 5

            if distance == previous_dist:
                speeds[side] = base_speed
                speeds[side-1] = base_speed

            # out of range correction
            if distance < 0.15 and distance < previous_dist + .01:
                speeds[side] = base_speed + 10
                speeds[side-1] = base_speed - 10
            if distance < 0.15 and distance > previous_dist:
                speeds[side] = base_speed
                speeds[side-1] = base_speed

            if distance > 0.20 and distance > previous_dist - 0.01:
                speeds[side] = base_speed - 10
                speeds[side-1] = base_speed + 10
            if distance > 0.20 and distance < previous_dist:
                speeds[side] = base_speed
                speeds[side-1] = base_speed

            forward(speeds[0], speeds[1])

            previous_dist = distance

            sleep(0.1)

    except KeyboardInterrupt:
        brake()
        pass

    except Exception:
        brake()
        pass

def cleanup_board():
    left_white.stop()
    left_red.stop()
    right_white.stop()
    right_red.stop()

    FLServo.stop()
    FRServo.stop()
    BLServo.stop()
    BRServo.stop()
    GPIO.cleanup()

cleanup_board()


'''

# Functions to check for if JS to PYTHON POST request worked
def forward(left_speed, right_speed):
    print("moved forward")

def backward(left_speed, right_speed):
    print("moved backward")

'''