"""player_driver controller."""

from controller import Robot, Receiver
from struct import pack, unpack
import sys

class Player(Robot):
    """
    Player object class
    """
    def __init__(self):
        super(Player, self).__init__()
        self.timeStep = 32  # set the control time step
        self.max_speed = 6.28
        self.id = int(sys.argv[1])

        self.ball_pos_receiver = self.getDevice("ball_pos_receiver") # channel - 0
        self.player_pos_receiver = self.getDevice("player_positions_receiver") # channel - 1
        self.emitter = self.getDevice("emitter") # channel - 0
        self.gps = self.getDevice("gps") # gps - to get self position
        self.left_motor = self.getDevice('motor_1')
        self.right_motor = self.getDevice('motor_2')

        self.ball_pos_receiver.enable(self.timeStep)
        self.player_pos_receiver.enable(self.timeStep)
        self.gps.enable(self.timeStep)

        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0.0)

    def recieveBallPosition(self):
        ballPos = -1
        if self.ball_pos_receiver.getQueueLength() > 0: # If receiver queue is not empty
            receivedData = self.ball_pos_receiver.getData()
            ballPos = unpack('2d', receivedData) # Parse data into character

            # if tup[0].decode("utf-8") == 'L': # 'L' means lack of progress occurred
            #     print("Detected Lack of Progress!")
            self.ball_pos_receiver.nextPacket() # Discard the current data packet

        return ballPos

    def receivePlayerPositions(self):
        playerPositions = {}
        while self.player_pos_receiver.getQueueLength() > 0: # If receiver queue is not empty
            receivedData = self.player_pos_receiver.getData()
            parsedData = unpack('i3d', receivedData) # Parse data into character
            playerPositions[parsedData[0]] = parsedData[1:]

            # if tup[0].decode("utf-8") == 'L': # 'L' means lack of progress occurred
            #     print("Detected Lack of Progress!")
            self.player_pos_receiver.nextPacket() # Discard the current data packet

        return playerPositions

    def emittSelfPosition(self):
        # Data send - id, x, y, z
        cur_pos = self.gps.getValues()
        byteData = pack('i3d', self.id, *cur_pos)
        self.emitter.send(byteData)

        print("\tSelf Position:", cur_pos)

    def action_1(self):
        pass

    # ... need to define various actions

    def run(self):
        while self.step(self.timeStep) != -1:
            self.left_speed = self.max_speed
            self.right_speed = self.max_speed

            self.left_motor.setVelocity(self.left_speed)
            self.right_motor.setVelocity(self.right_speed)

            # Print values
            if self.id == 0: print("\n", "-"*10)
            print("Player {}:".format(str(self.id)))

            self.emittSelfPosition()
            print("\tBall Position:", self.recieveBallPosition())
            print("\tOther Player Positions:\n")
            playerPositions = self.receivePlayerPositions()
            for id in playerPositions:
                print("\t\t", id, ":", playerPositions[id])


if __name__ == "__main__":
    player = Player()
    player.run()
