import cv2
import pygame
import time
from pygame.locals import *

# Access the USB camera (adjust the camera index if needed)
video_capture = cv2.VideoCapture(0)

# Initialize pygame
pygame.init()

# Set the window size to match the camera frame
width, height = int(video_capture.get(3)), int(video_capture.get(4))
window = pygame.display.set_mode((width, height))

while True:
    ret, frame = video_capture.read()  # Read a frame from the camera

    # Convert the OpenCV frame to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pygame_frame = pygame.surfarray.make_surface(frame)

    # Display the Pygame surface on the window
    window.blit(pygame_frame, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            # Release the camera and close the window on window close
            video_capture.release()
            pygame.quit()
            cv2.destroyAllWindows()
            exit()

    # Introduce a delay (equivalent to cv2.waitKey(1))
    time.sleep(0.01)

    # Check for 'q' key press
    keys = pygame.key.get_pressed()
    if keys[K_q]:
        break

# Release the camera and close the window when 'q' key is pressed
video_capture.release()
pygame.quit()
cv2.destroyAllWindows()