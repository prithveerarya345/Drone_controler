# This code is based on the tutorial by Murtaza's Workshop - Robotics and AI
# Tutorial: https://youtu.be/LmEcyQnfpDA

import keypressmodule
import pygame
pygame.init()
from djitellopy import tello
import keypressmodule as kp
import cv2
import time
import numpy as np
import math

# Define constants for drone movement
fSpeed = 117/10 # Forward speed in cm/s
aSpeed = 360/10 # Angular speed in deg/s
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval
x, y = 500, 500
a = 0
yaw = 0

# Initialize key press module and connect to Tello drone
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img

me.streamon()

def keyboard_inp():
    """Handle keyboard input for drone control and mapping"""
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    d = 0
    global x, y, yaw, a
    
    # Check for various key presses and update movement variables
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"): 
        lr = speed
        d = -dInterval
        a = 180
    
    if kp.getKey("UP"): 
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"): 
        fb = -speed  
        d = -dInterval
        a = -90
    
    if kp.getKey("w"): 
        ud = speed
    elif kp.getKey("s"): 
        ud = -speed 
    
    if kp.getKey("a"): 
        yv = aspeed
        yaw -= aInterval
    elif kp.getKey("d"): 
        yv = -aspeed 
        yaw += aInterval
    
    if kp.getKey("q"):
        yv = me.land()
    if kp.getKey("e"):
        yv = me.takeoff()
    
    if kp.getKey('z'):
        cv2.imwrite(f'Images/{time.time}.jpg',img)
        time.sleep(0.3)
    
    time.sleep(interval)     
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))
     
    return [lr, fb, ud, yv, x, y]

me.takeoff()

def drawPoints(img, points):
    """Draw points on the mapping image"""
    for point in points:
        cv2.circle(img, point, 5, (0,0,255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img,f'({(points[-1][0]-500)/100}, {(points[-1][1]-500)/100})m',
                (points[-1][0]+10,points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1)

points = [(0,0), (0,0)]

# Main loop for mapping
while True:
    vals = keyboard_inp()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)