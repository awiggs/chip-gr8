###########################################
#---------------- Pong AI ----------------#
#                                         #
# Tries to keep the ball aligned with the #
# paddle.                                 #
###########################################


# Imports
import random
import chipgr8
from chipgr8 import *
from chipgr8.games import Game


# Global Variables
rate = 1
vm = None 
paddleY = 0
ballPos = (0,0)


# Pong Game Object
pong = Game(
    ROM      = 'Pong (1 player)',
    observer = Observer()
        .addQuery('p1Score',     Query(addr=755))
        .addQuery('p2Score',     Query(addr=756))
        .addQuery('myY',         Query(addr=379))
        .addQuery('ballX',       Query(addr=374))
        .addQuery('ballY',       Query(addr=375))
        .addQuery('done',        lambda o, vm: o.p1Score >= 9 or o.p2Score >= 9),
    actions  = NamedList(
        ['none',   'up', 'down'],
        [ K_NONE,   K_1,  K_4  ],
    ),
)


# Runs the AI algorithm for the Breakout game 
def pongAgent():
    global vm
    vm = chipgr8.init(display=True, ROM=pong.ROM, sampleRate=rate, speed=100)
    vm.VM.seed = random.randint(0, 255)

    # wait for the game to load
    waitToLoad(1000)

    # Perform AI logic
    while not vm.done():
        vm.doneIf(pong.observe(vm).done)
        # Get the position of the paddle and the ball
        setPositions()

        # Try to stay aligned with the ball
        if ballAboveMe():
            moveUp()
        elif ballBelowMe():
            moveDown()
        else:
            stayStill()


# Wait 't' clock cycles
def waitToLoad(t):
    for _ in range(t):
        vm.act(pong.actions.none)


# Sets the global position variables to their current values
def setPositions():
    global paddleY
    global ballPos
    observations = pong.observe(vm)
    paddleY = observations.myY
    ballPos = (observations.ballX, observations.ballY)


# Checks if the ball is currently to the left of the paddle's central pixels
def ballAboveMe():
    return (ballPos[1] < paddleY + 1) or (ballPos[1] < paddleY + 4) # The paddle is 6 pixels wide, this checks both sides of the dead zone


# Checks if the ball is currently to the right of the paddle's central pixels
def ballBelowMe():
    return (ballPos[1] > paddleY + 1) or (ballPos[1] > paddleY + 4) # The paddle is 6 pixels wide, this checks both sides of the dead zone


# Moves the paddle 1 pixel to the left
def moveUp():
    if paddleY != 0:
        vm.actUntil(pong.actions.up, paddleMoved)
    else:
        stayStill()    


# Moves the paddle 1 pixel to the right
def moveDown():
    if paddleY != 26:
        vm.actUntil(pong.actions.down, paddleMoved)
    else:
        stayStill()


# The paddle takes no actions
def stayStill():
    vm.act(pong.actions.none)


# Checks if the paddle has moved yet
def paddleMoved(vm):
    observations = pong.observe(vm)
    return paddleY != observations.myY or observations.done


# Start the algorithm
if __name__ == '__main__':
    pongAgent()
