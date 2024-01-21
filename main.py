#!/usr/bin/env python

from flask import Flask
import os
from math import cos, sin, pi, floor
import pygame
# from rplidar import RPLidar
import math
import time

import fire_sensing as fsense
import webserver as wb
import lidar as lidar_sensor

# wb.startWebserver()



# lidar = RPLidar('/dev/ttyUSB0')
# map_points = []
# scan_duration = 3

# lidar_sensor.full_burst_scan_cycle(lidar, map_points, scan_duration)
# lidar_sensor.full_burst_scan_cycle(lidar, map_points, scan_duration)

# lidar.disconnect()

# RPI's IP
#192.168.71.207