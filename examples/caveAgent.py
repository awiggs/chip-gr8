###########################################
#---------------- CAVE AI ----------------#
#                                         #
# Hugs the wall on its right and, using   #
# a classic maze solving strategy to      #
# escape.                                 #
###########################################


# Imports
import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
from chipgr8.games import Cave as cave


# Global Variables
rate = 1
vm = chipgr8.init(display=True, ROM=cave.ROM, sampleRate=rate)
position = (0,0)
direction = "down"
preferredTurn = "right"


# Solves the Cave game
def start():
    global position

    # wait for the title screen to load
    waitToLoad(1000)

    # start the game
    vm.act(cave.actions.start)

    # wait for the first playable scene to load
    waitToLoad(1000)

    # Reach the first wall by going down and turn left to get a wall on our right side
    while not vm.done():
        position = getPosition()
        if canMoveForward():
            moveForward()
        else:
            turnLeft()
            break

    # We are against a wall: begin wall hugging logic
    while not vm.done():
        position = getPosition()
        if rightSideIsWall(): # If we have a wall on our right we want to move forward if possible
            if canMoveForward():
                moveForward()
            else:
                turnLeft() # We have a wall on our right, but we cant go foward, so we must go left
        else:
            turnRight() # We have lost our wall, turning right and going 1 step forward should find it again
            moveForward()


# Takes a direction and moves the player token 1 step in that direction   
def move(s):
    if s == "up":
        vm.actUntil(cave.actions.up, positionChanged)
    elif s == "right":
        vm.actUntil(cave.actions.right, positionChanged)
    elif s == "down":
        vm.actUntil(cave.actions.down, positionChanged)
    elif s == "left":
        vm.actUntil(cave.actions.left, positionChanged)
    else:
        raise Exception("Invalid direction for movement.\nCan only move left/right/up/down")


# Moves the player 1 step forwards (relative to the player)
def moveForward():
    if direction == "left":
        move("left")
    elif direction == "right":
        move("right")
    elif direction == "up":
        move("up")
    elif direction == "down":
        move("down")


# Turn the player 90 degrees to the right
def turnRight():
    global direction
    if direction == "left":
        direction = "up"
    elif direction == "right":
        direction = "down"
    elif direction == "up":
        direction = "right"
    elif direction == "down":
        direction = "left"


# Turn the player 90 degrees to the left
def turnLeft():
    global direction
    if direction == "left":
        direction = "down"
    elif direction == "right":
        direction = "up"
    elif direction == "up":
        direction = "left"
    elif direction == "down":
        direction = "right"


# Check if there is a wall infront of the player
def canMoveForward():
    global position
    try:
        position = getPosition()
        if direction == "left":
            return vm.ctx()[position[0] - 1, position[1]] == 0
        if direction == "right":
            return vm.ctx()[position[0] + 1, position[1]] == 0
        if direction == "up":
            return vm.ctx()[position[0], position[1] - 1] == 0
        if direction == "down":
            return vm.ctx()[position[0], position[1] + 1] == 0
    except:
        waitToLoad(500)
        return True


# Check if the square on the player's left is safe
def canMoveLeft():
    global position
    if direction == "left":
        return vm.ctx()[position[0], position[1] + 1] == 0
    if direction == "right":
        return vm.ctx()[position[0], position[1] - 1] == 0
    if direction == "up":
        return vm.ctx()[position[0] - 1, position[1]] == 0
    if direction == "down":
        return vm.ctx()[position[0] + 1, position[1]] == 0


# Check if the player's position has changed
def positionChanged(vm):
    observations = cave.observe(vm)
    return position[0] != observations.myX or position[1] != observations.myY


# Wait 't' clock cycles
def waitToLoad(t):
    for _ in range(t):
        vm.act(cave.actions.none)


# Returns a tuple of the players X and Y coordinates
def getPosition():
    observations = cave.observe(vm)
    return (observations.myX, observations.myY)


# Checks if the player has a wall on their right side
def rightSideIsWall():
    if direction == "left":
        return vm.ctx()[position[0], position[1] - 1] == 1
    if direction == "right":
        return vm.ctx()[position[0], position[1] + 1] == 1
    if direction == "up":
        return vm.ctx()[position[0] + 1, position[1]] == 1
    if direction == "down":
        return vm.ctx()[position[0] - 1, position[1]] == 1


# Start the algorithm
start()