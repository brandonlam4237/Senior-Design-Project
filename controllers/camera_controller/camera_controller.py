"""camera_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Camera
import numpy as np
import cv2
# import codecs, json
# import time

# create the Robot instance.
robot = Robot()

timestep = int(robot.getBasicTimeStep())
ballRadiusUnits = 0.1

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

camera = Camera("CAM")
camera.enable(timestep)
# camera.recognitionEnable(timestep)

cameraWidth = camera.getWidth()
cameraHeight = camera.getHeight()

def getBallPosition(img):
    "Returns pixel center location of ball from image"

    # Color code - BGR
    lower = np.array([0, 0, 50]) # lower bound values for color
    upper = np.array([50, 50, 255]) # upper bound values for color

    # Returns all indices x and y in the 2d array where the color of the pixel
    # falls with in the defined threshold, which defines the ball.
    Y, X = np.where(cv2.inRange(img, lower, upper) != 0)
    # ball position in pixels
    xPixel, yPixel = np.median(X), np.median(Y)

    # use ball pixels and defined radius to calculate units per pixel
    ballRadiusPixels = (np.max(X) - np.min(X) + 1) / 2
    unitsInPixel = ballRadiusUnits / ballRadiusPixels

    # convert pixel values to coordinate values
    x = unitsInPixel * (xPixel - ((cameraWidth / 2) - 0.5))
    z = unitsInPixel * (yPixel - ((cameraHeight / 2) - 0.5))
    return x, z

doOnce = True
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:

    cameraData = camera.getImage();
    image = np.frombuffer(cameraData, np.uint8).reshape((cameraHeight, cameraWidth, 4)) # get np array
    img_float32 = np.float32(image)
    bgr_img = cv2.cvtColor(img_float32, cv2.COLOR_BGRA2BGR) # convert from BGRA to BGR color format

    ballPos = getBallPosition(bgr_img)
    print("Ball position:", ballPos)

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    # pass

# Enter here exit cleanup code.
