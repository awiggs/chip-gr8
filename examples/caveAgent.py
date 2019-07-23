import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
from chipgr8.games import Cave as cave

# Globals
rate = 1
vm = chipgr8.init(display=True, ROM=cave.ROM, sampleRate=rate)
position = (0,0)
direction = "down"
preferredTurn = "right"

def start():
    global position

    # wait for the game to finish loading
    waitToLoad(1000)

    # start the game
    vm.act(cave.actions.start)

    waitToLoad(1000)

    # Reach the first wall by going down
    while not vm.done():
        if canMoveForward():
            moveForward()
        else:
            turnLeft()
            break

    # We are against a wall: begin wall hugging logic
    while not vm.done():
        if rightSideIsWall():
            if canMoveForward():
                moveForward()
            else:
                turnLeft()
        else:
            turnRight()
            moveForward()
        

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

def moveForward():
    if direction == "left":
        move("left")
    elif direction == "right":
        move("right")
    elif direction == "up":
        move("up")
    elif direction == "down":
        move("down")

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

def positionChanged(vm):
    observations = cave.observe(vm)
    return position[0] != observations.myX or position[1] != observations.myY

def waitToLoad(t):
    for _ in range(t):
        vm.act(cave.actions.none)

def getPosition():
    observations = cave.observe(vm)
    return (observations.myX, observations.myY)

def rightSideIsWall():
    if direction == "left":
        return vm.ctx()[position[0], position[1] - 1] == 1
    if direction == "right":
        return vm.ctx()[position[0], position[1] + 1] == 1
    if direction == "up":
        return vm.ctx()[position[0] + 1, position[1]] == 1
    if direction == "down":
        return vm.ctx()[position[0] - 1, position[1]] == 1

start()