
from pitop.pma import UltrasonicSensor
import RPi.GPIO as GPIO
from time import sleep

print("Setting up board")
GPIO.setmode(GPIO.BCM)
print("board set up")

LL = 19
LR = 26
RL = 20
RR = 21
GPIO.setup(LL, GPIO.OUT)
GPIO.setup(LR, GPIO.OUT)
GPIO.setup(RL, GPIO.OUT)
GPIO.setup(RR, GPIO.OUT)

frequency = 1000

left_white = GPIO.PWM(LL, frequency)
left_red = GPIO.PWM(LR, frequency)

right_white = GPIO.PWM(RL, frequency)
right_red = GPIO.PWM(RR, frequency)

left_white.start(0)
left_red.start(0)
right_white.start(0)
right_red.start(0)

print("Pins set up")

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

# commands
def move_forward_amount(speed, time):
    forward(speed, speed)
    sleep(time)
    brake()

def move_backward_amount(speed, time):
    backward(speed, speed)
    sleep(time)
    brake()

# Set up the components
left = UltrasonicSensor("D7")
right = UltrasonicSensor("D0")
front = UltrasonicSensor("D3")

side = 1 # 0 is left, 1 is right

sensors = [left, right]

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
    GPIO.cleanup()

cleanup_board()


'''

# Functions to check for if JS to PYTHON POST request worked
def forward(left_speed, right_speed):
    print("moved forward")

def backward(left_speed, right_speed):
    print("moved backward")

'''