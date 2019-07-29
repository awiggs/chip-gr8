###########################################
#---------------- CAVE AI ----------------#
#                                         #
# Hugs the wall on its right and, using   #
# a classic maze solving strategy to      #
# escape.                                 #
###########################################


# TODO remove once pip install is working
import sys, os
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))

# Imports
import chipgr8
from chipgr8.games import Cave


# Global Variables
vm = None
position = (0,0)
direction = 'down'

# Solves the Cave game
def caveAgent():
    global vm, position
    vm = chipgr8.init(display=True, ROM=Cave.ROM, sampleRate=1)

    # wait for the title screen to load
    waitToLoad(1000)

    # start the game
    vm.act(Cave.actions.start)

    # wait for the first playable scene to load
    waitToLoad(1000)

    # Reach the first wall by going down and turn left to get a wall on our right side
    while not vm.done():
        obs = Cave.observe(vm)
        position = getPosition(obs)
        if canMoveForward():
            moveForward()
        else:
            turnLeft()
            break

    # We are against a wall: begin wall hugging logic
    while not vm.done():
        obs = Cave.observe(vm)
        position = getPosition(obs)
        vm.doneIf(obs.done)
        # If we have a wall on our right we want to move forward if possible
        if rightSideIsWall(obs): 
            if canMoveForward():
                moveForward()
            else:
                # We have a wall on our right, but we cant go foward, so we must go left
                turnLeft() 
        else:
            # We have lost our wall, turning right and going 1 step forward should find it again
            turnRight() 
            moveForward()

def waitToLoad(t):
    '''
    Wait `t` clock cycles
    '''
    vm.act(Cave.actions.none, repeat=t)

def getPosition(obs):
    '''
    Returns a tuple of the players X and Y coordinates
    '''
    return (obs.x, obs.y)

def move(direction):
    '''
    Takes a direction and moves the player token 1 step in that direction  
    '''
    vm.actUntil(Cave.actions[direction], positionChanged)

def positionChanged(vm):
    '''
    Check if the player's position has changed
    '''
    obs = Cave.observe(vm)
    return position != getPosition(obs) or obs.done

def moveForward():
    '''
    Moves the player 1 step forwards (relative to the player)
    '''
    move(direction)

def turnRight():
    '''
    Turn the player 90 degrees to the right
    '''
    global direction
    if direction == 'left':
        direction = 'up'
    elif direction == 'right':
        direction = 'down'
    elif direction == 'up':
        direction = 'right'
    elif direction == 'down':
        direction = 'left'

def turnLeft():
    '''
    Turn the player 90 degrees to the left
    '''
    global direction
    if direction == 'left':
        direction = 'down'
    elif direction == 'right':
        direction = 'up'
    elif direction == 'up':
        direction = 'left'
    elif direction == 'down':
        direction = 'right'

def canMoveForward():
    '''
    Check if there is a wall infront of the player
    '''
    x, y = position
    try:
        if direction == 'left':
            return not vm.ctx()[x - 1, y]
        if direction == 'right':
            return not vm.ctx()[x + 1, y]
        if direction == 'up':
            return not vm.ctx()[x, y - 1]
        if direction == 'down':
            return not vm.ctx()[x, y + 1]
    except IndexError:
        waitToLoad(500)
        return True

def rightSideIsWall(obs):
    '''
    Checks if the player has a wall on their right side
    '''
    if direction == 'left':
        return not obs.upClear
    if direction == 'right':
        return not obs.downClear
    if direction == 'up':
        return not obs.rightClear
    if direction == 'down':
        return not obs.leftClear

# Start the algorithm
if __name__ == '__main__':
    caveAgent()