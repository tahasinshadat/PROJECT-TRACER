
from pitop.pma import UltrasonicSensor
import RPi.GPIO as GPIO
from time import sleep
import math

from movement_math import convert_range, get_DC_from_angle

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
    
side_front = UltrasonicSensor("D4")
side_back = UltrasonicSensor("D7")
front = UltrasonicSensor("D3")
back = UltrasonicSensor("D0")

#########
# Setup #
#########

direction = 0
direction_sensors = (front, back)
driving_function = (clockwise, counter_clockwise)

# Combined motor functions
def drive_motor(left : GPIO.PWM, right: GPIO.PWM, speed, direction):
    if speed > 0:
        driving_function[direction](left, right, speed)
    else:
        driving_function[direction-1](left, right, speed)

def drive_all(direction, front_left_spd, front_right_spd, back_left_spd, back_right_spd):
    drive_motor(FLL, FLR, front_left_spd, direction)
    drive_motor(FRL, FRR, front_right_spd, direction)
    # drive_motor(BLL, BLR, back_left_spd, direction)
    # drive_motor(BRL, BRR, back_right_spd, direction)

# side = 0 # 0 is right, 1 is left # Single side ultrasonic

sensors = [side_front, side_back]

TARGET_DIST_IN = 3
TARGET_DIST_CM = TARGET_DIST_IN * 2.54
SENSOR_GAP_IN = 13 # IN
SENSOR_GAP_CM = SENSOR_GAP_IN * 2.54
BASE_SPEED = 25
motor_speeds = [BASE_SPEED, BASE_SPEED, BASE_SPEED, BASE_SPEED] # FL, FR, BL, BR

# speeds = [BASE_SPEED, BASE_SPEED] # DIFFERENTIAL: left, right

# cycle = 0

# previous_dist = sensors[side].distance # Single side Ultrasonic

def auto_drive():
    try:
        # Swerve drive
        
        # readings
        front_dist = direction_sensors[direction].distance
        side_front_dist = side_front.distance
        side_back_dist = side_back.distance

        if front_dist < 5 * 2.54:
            raise Exception

        # auto parallel
        current_angle = math.degrees(math.acos((side_back_dist - side_front_dist) / SENSOR_GAP_CM))
        correction_angle = 90-current_angle

        # auto distance
        wall_dist = (side_front_dist + side_back_dist) / 2 # average
        correction_dist = TARGET_DIST_CM-wall_dist
        correct_dist_angle = convert_range(correction_dist, 0, TARGET_DIST_CM, 0, 45)
        correction_angle += correct_dist_angle
        
        if abs(correction_angle) > 45:
            correction_angle = math.copysign(45, current_angle)

        FLServo.ChangeDutyCycle(get_DC_from_angle(correction_angle))
        FRServo.ChangeDutyCycle(get_DC_from_angle(correction_angle))
        BLServo.ChangeDutyCycle(get_DC_from_angle(-correction_angle))
        BRServo.ChangeDutyCycle(get_DC_from_angle(-correction_angle))

        drive_all(direction, *motor_speeds)

        """# Differential drive
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

            sleep(0.1)"""

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

def main():
    auto_drive()
    cleanup_board()

if __name__ == "__main__":
    main()


'''

# Functions to check for if JS to PYTHON POST request worked
def forward(left_speed, right_speed):
    print("moved forward")

def backward(left_speed, right_speed):
    print("moved backward")

'''