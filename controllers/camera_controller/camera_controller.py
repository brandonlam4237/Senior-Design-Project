"""camera_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera
import numpy as np
# import cv2
# import time
#
#
def getBallPosition(im):
    "Returns pixel center location of ball from image"
    # Returns all indices x and y in the 2d array where the red is the main color, which defines the ball.
    Y, X = np.where(np.logical_and.reduce((250 <= im[:,:,2], im[:,:,2] <= 255, im[:,:,0] < 50, im[:,:,1] < 50)))
    # ballRadius = np.max(X) - np.min(X) + 1
    return np.median(X), np.median(Y)

def getCurTime():
    return round(time.time()*1000)

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64 #int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

camera = Camera("CAM")
camera.enable(timestep)
# camera.recognitionEnable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller

# prevTime = getCurTime()
do = True

while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:

    cameraData = camera.getImage();
    image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    print(getBallPosition(image))



    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    # pass

# Enter here exit cleanup code.
