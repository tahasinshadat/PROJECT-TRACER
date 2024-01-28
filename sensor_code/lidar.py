from rplidar import RPLidar
import pygame
import math
import time

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RPLidar Scanner")

# Function to start scanning and store points in the provided list for a specified duration
def burst_scan(lidar, points_list, scan_duration):
    lidar.start_motor()

    start_time = time.time()
    end_time = start_time + scan_duration

    for scan in lidar.iter_scans():
        current_time = time.time()

        for (_, angle, distance) in scan:
            x = distance * math.cos(math.radians(angle))
            y = distance * math.sin(math.radians(angle))
            points_list.append((x, y))
            
            
        # No need for real time plotting. My plan is to have bursts of lidar scans, and then update the map every few seconds. This helps address the too many bytes error.
        """

        # Display points in real-time (causes byte errors sometimes)
        screen.fill((0, 0, 0))  # Clear screen
        for point in points_list:
            pygame.draw.circle(screen, (255, 255, 255), (int(point[0]) + width // 2, int(point[1]) + height // 2), 1)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_scanning(lidar)
                pygame.quit()
                lidar.stop_motor()
                lidar.disconnect()
                exit()
                
        """
        
        if current_time >= end_time:
            break
        
    stop_scanning(lidar)

# Function to display scanned points on Pygame
def display_map_data(points_list):
    screen.fill((0, 0, 0))  # Clear screen
    for point in points_list:
        pygame.draw.circle(screen, (255, 255, 255), (int(point[0]) + width // 2, int(point[1]) + height // 2), 1)
    pygame.display.flip()

# Function to stop scanning
def stop_scanning(lidar):
    lidar.stop()
    lidar.stop_motor()

def full_burst_scan_cycle(lidar, map_points, scan_duration):
    burst_scan(lidar, map_points, scan_duration)
    display_map_data(map_points)
    time.sleep(3)

"""
 # CODE I REFERENCED - simply spins the lidar and gets points from it
 
from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
"""
