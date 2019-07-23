###########################################
#-------------- Breakout AI --------------#
#                                         #
# Tries to keep the ball aligned with the #
# paddle. Consider's itself as aligned    #
# when the ball is anywhere in the 4      #
# central pixels of the paddle. Prevents  #
# the paddle from wrapping because that   #
# confuses the AI.                        #
###########################################


# Imports
import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
from chipgr8.games import Breakout


# Global Variables
rate = 1
vm = chipgr8.init(display=True, ROM=Breakout.ROM, sampleRate=rate)
paddleX = 0
ballPos = (0,0)


# Runs the AI algorithm for the Breakout game 
def start():

    # wait for the game to load
    waitToLoad(1000)

    # Perform AI logic
    while not vm.done():
        # Get the position of the paddle and the ball
        setPositions()

        # Try to stay aligned with the ball
        if ballLeftOfMe():
            moveLeft()
        elif ballRightOfMe():
            moveRight()
        else:
            stayStill()


# Wait 't' clock cycles
def waitToLoad(t):
    for _ in range(t):
        vm.act(Breakout.actions.none)


# Sets the global position variables to their current values
def setPositions():
    global paddleX
    global ballPos
    observations = Breakout.observe(vm)
    paddleX = observations.myX
    ballPos = (observations.ballX, observations.ballY)


# Checks if the ball is currently to the left of the paddle's central pixels
def ballLeftOfMe():
    return (ballPos[0] < paddleX + 1) or (ballPos[0] < paddleX + 4) # The paddle is 6 pixels wide, this checks both sides of the dead zone


# Checks if the ball is currently to the right of the paddle's central pixels
def ballRightOfMe():
    return (ballPos[0] > paddleX + 1) or (ballPos[0] > paddleX + 4) # The paddle is 6 pixels wide, this checks both sides of the dead zone


# Moves the paddle 1 pixel to the left
def moveLeft():
    if paddleX != 0:
        vm.actUntil(Breakout.actions.left, paddleMoved)
    else:
        stayStill()    


# Moves the paddle 1 pixel to the right
def moveRight():
    if paddleX != 58:
        vm.actUntil(Breakout.actions.right, paddleMoved)
    else:
        stayStill()


# The paddle takes no actions
def stayStill():
    vm.act(Breakout.actions.none)


# Checks if the paddle has moved yet
def paddleMoved(vm):
    observations = Breakout.observe(vm)
    return paddleX != observations.myX


# Start the algorithm
start()
