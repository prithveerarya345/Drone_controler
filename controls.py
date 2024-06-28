# This code is based on the tutorial by Murtaza's Workshop - Robotics and AI
# Tutorial: https://youtu.be/LmEcyQnfpDA

from djitellopy import tello
import keypressmodule as kp
import cv2
import time

# Initialize key press module
kp.init()

# Create Tello drone object and connect
me = tello.Tello()
me.connect()
print(me.get_battery())

# Global variable for image
global img

# Start video stream
me.streamon()

def keyboard_inp():
    """Handle keyboard input for drone control"""
    lr, fb, ud, yv = 0, 0, 0, 0  # Initialize movement variables
    speed = 50  # Set speed for movement
    
    # Check for left/right movement
    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"): 
        lr = speed
    
    # Check for forward/backward movement
    if kp.getKey("UP"): 
        fb = speed
    elif kp.getKey("DOWN"): 
        fb = -speed  
    
    # Check for up/down movement
    if kp.getKey("w"): 
        ud = speed
    elif kp.getKey("s"): 
        ud = -speed 
    
    # Check for yaw rotation
    if kp.getKey("a"): 
        yv = speed
    elif kp.getKey("d"): 
        yv = -speed 
    
    # Check for landing and takeoff
    if kp.getKey("q"):
        yv = me.land()
    if kp.getKey("e"):
        yv = me.takeoff()
    
    # Capture image on 'z' key press
    if kp.getKey('z'):
        cv2.imwrite(f'Images/{time.time}.jpg',img)
        time.sleep(0.3)
    
    return [lr, fb, ud, yv]

# Takeoff the drone
me.takeoff()

# Main control loop
while True:
    vals = keyboard_inp()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)