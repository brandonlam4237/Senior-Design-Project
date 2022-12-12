"""
camera_controller controller
Gets ball position from camera image and emitts data on channel 1
"""

from controller import Robot, Camera, Emitter
import numpy as np
import cv2
from struct import pack

# create the Robot instance.
robot = Robot()

timestep = int(robot.getBasicTimeStep()) # 32
ballRadiusUnits = 0.1

camera = Camera("CAM")
emitter = robot.getDevice("emitter")

camera.enable(timestep)

cameraWidth = camera.getWidth()
cameraHeight = camera.getHeight()

def getBallPosition(img):
    "Returns pixel center location of ball from image"

    # Color code - BGR
    lower = np.array([0, 0, 65]) # lower bound values for color
    upper = np.array([50, 50, 255]) # upper bound values for color

    # Returns all indices x and y in the 2d array where the color of the pixel
    # falls with in the defined threshold, which defines the ball.
    Y, X = np.where(cv2.inRange(img, lower, upper))
    # ball position in pixels
    xPixel, yPixel = np.median(X), np.median(Y)

    # use ball pixels and defined radius to calculate units per pixel
    ballRadiusPixels = (np.max(X) - np.min(X) + 1) / 2
    unitsPerPixel = ballRadiusUnits / ballRadiusPixels

    # convert pixel values to coordinate values
    x = unitsPerPixel * (xPixel - ((cameraWidth / 2) - 0.5))
    z = unitsPerPixel * (yPixel - ((cameraHeight / 2) - 0.5))

    return x, z

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    cameraData = camera.getImage();
    image = np.frombuffer(cameraData, np.uint8).reshape((cameraHeight, cameraWidth, 4)) # get np array
    img_float32 = np.float32(image)
    bgr_img = cv2.cvtColor(img_float32, cv2.COLOR_BGRA2BGR) # convert from BGRA to BGR color format

    ballPos = getBallPosition(bgr_img)
    byteData = pack('2d', *ballPos)
    emitter.send(byteData)


# Enter here exit cleanup code.
