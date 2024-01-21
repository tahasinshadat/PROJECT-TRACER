################################################################################################################################################
#
#       INSTALL DEPENDENCIES + IMPORTANT INFO
#
################################################################################################################################################
# run pip install opencv-python-headless flask
from flask import Flask, render_template, Response, request
import cv2
import movement
from flask_socketio import SocketIO, emit
from OpenSSL import SSL
import base64
import numpy as np
import pygame
import threading
import sys

################################################################################################################################################
#
#       INITIALIZE FLASK AND SOCKETIO
#
################################################################################################################################################
app = Flask(__name__)
socketio = SocketIO(app)



################################################################################################################################################
#
#       INITIALIZE PYGAME AND RELEVANT FUNCTIONS
#
################################################################################################################################################
pygame.init()

screen_info = pygame.display.Info() # Get the screen dimensions for full size

screen_width, screen_height = screen_info.current_w - 100, screen_info.current_h - 100

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Client Camera Stream')

def update_window(img):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize the image to fit the screen (reverse width and height because I rotated the image)
    resized_img = cv2.resize(img_rgb, (screen_height, screen_width))

    # Convert the OpenCV frame to a Pygame surface
    pygame_frame = pygame.surfarray.make_surface(resized_img)

    # Display the Pygame surface on the window
    window.blit(pygame_frame, (0, 0))
    pygame.display.update()



################################################################################################################################################
#
#       VIDEO CAPTURE
#
################################################################################################################################################
video_capture_1 = cv2.VideoCapture(1)
video_capture_2 = cv2.VideoCapture(2)
current_camera = video_capture_1  # Initial camera

def generate_frames():
    while True:
        success, frame = current_camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



################################################################################################################################################
#
#       WEBSERVER ROUTING (Create routes for diff URLS of website)
#
################################################################################################################################################
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/controlPanel")
def controlPanel():
    return render_template('controlPanel.html')

@app.route('/video') # Video from the ROBOT
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') # Return the response generated from the frames



################################################################################################################################################
#
#       POST REQUESTS / BACKEND SERVERSIDE OPERATIONS
#
################################################################################################################################################
# Manually control TRACER from website terminal
@app.route('/move', methods=['POST'])
def move():
    command = request.form['command'] # Retrieves the 'command' data from the POST request
    if command == 't-forward':
        movement.forward(50, 50) 
    elif command == 't-backward':
        movement.backward(50, 50) 
    else:
        return "Invalid command", 400
    return "Movement command executed successfully" # Return response to Users Terminal if POST request successfully went through to robot

# New route for camera switch
@app.route('/switch_camera', methods=['POST'])
def switch_camera():
    global current_camera
    if current_camera == video_capture_1:
        current_camera = video_capture_2
    else:
        current_camera = video_capture_1
    return "Camera switched successfully"



################################################################################################################################################
#
#       SERVER TO CLIENT AND CLIENT TO SERVER COMMUNICATIONS (SocketIO event handlers for WebRTC Communication)
#
################################################################################################################################################
@socketio.on('user_offer')
def handle_user_offer(offer):
    emit('server_offer', offer, broadcast=True)

@socketio.on('server_answer')
def handle_server_answer(answer):
    emit('user_answer', answer, broadcast=True)

@socketio.on('user_ice_candidate')
def handle_user_ice_candidate(candidate):
    emit('server_ice_candidate', candidate, broadcast=True)

@socketio.on('server_ice_candidate')
def handle_server_ice_candidate(candidate):
    emit('user_ice_candidate', candidate, broadcast=True)

# Decode base64 image and perform necessary actions -> ex: broadcast the frame to other clients
@socketio.on('user_camera_frame')
def handle_user_camera_frame(frame):
    # print('Received camera frame from user:', frame)
    try:
        # Decode base64 image
        encoded_data = frame.split(',')[1]
        decoded_frame = base64.b64decode(encoded_data)
        np_frame = np.frombuffer(decoded_frame, dtype=np.uint8)
        img = cv2.imdecode(np_frame, 1)

        if img is not None and img.size > 0:
            update_window(img)

    except Exception as e:
        print(f"Error handling user camera frame: {e}")



################################################################################################################################################
#
#       ABSTRACTION TO GET READY FOR EXPORT
#
################################################################################################################################################
def startWebserver():
    # app.run(host="0.0.0.0", port="5000")
    # Use the generated key and certificate files
    context = ('cert.pem', 'key.pem')  # Specify the certificate and key directly

    ssl_context = (context[0], context[1])

    # Run Flask and SocketIO in a separate thread
    socketio_thread = threading.Thread(target=socketio.run, kwargs={'app': app, 'host': '0.0.0.0', 'port': 5000, 'debug': False, 'use_reloader': False, 'allow_unsafe_werkzeug': True, 'ssl_context': ssl_context})
    socketio_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()  # Exit the entire program

            # Check for "q" key press
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
                socketio.stop()  # Stop the Flask-SocketIO server
                sys.exit()  # Exit the entire program

        pygame.display.update()

    pygame.quit()


# startWebserver()


'''
Because Im using web sockets to connect other clients to our webserver 
and send video feed over, I must host the website over a safe / trusted protocol like HTTPS or WS

Note:
- use the http-server package (install it using npm install -g http-server):

Run the following command:
- http-server -S -C cert.pem -K key.pem
Replace cert.pem and key.pem with your own SSL certificate and key.


To get my certificat ekey, must run either of these commands (I would do the bottom one cause I did that one, but apparently both work idk):
- openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
- openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

'''
