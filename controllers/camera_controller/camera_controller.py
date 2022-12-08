"""camera_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Camera
import time
# from controller import CameraRecognitionObject


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
    #  val = ds.getValue()
    # camera.getImage()
    if do:
        camera.saveImage("img.png", 100)
        # print(camera.getImageArray())
        # with open("imgData.py", "w") as f:
        #     f.write(str(camera.getImage()))
        # print(camera.getRecognitionNumberOfObjects())
        # print(dir(object.position_on_image.acquire))

        do = False

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
