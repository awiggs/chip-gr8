import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
from chipgr8.games import Cave as cave

# Globals
rate = 1
lastMove = None
vm = chipgr8.init(display=True, ROM=cave.ROM, sampleRate=rate)
xPos = 0
yPos = 0

def start():
    global rate
    global lastMove
    global vm
    global xPos
    global yPos

    # wait for the game to finish loading
    waitToLoad(1000)

    # start the game
    vm.act(cave.actions.start)

    waitToLoad(1000)

    #loop actions
    while not vm.done():

        # get new observations (x,y) position
        observations = cave.observe(vm)
        xPos = observations.myX
        yPos = observations.myY

        # get the value of my up,down,left,right
        try:
            up          = vm.ctx()[xPos, yPos - 1] == 0 # up is safe
            right       = vm.ctx()[xPos + 1, yPos] == 0 # right is safe
            down        = vm.ctx()[xPos, yPos + 1] == 0 # down is safe
            left        = vm.ctx()[xPos - 1, yPos] == 0 # left is safe
        except:
            move("right")
            waitToLoad(500)
            continue

        # Make decisions
        if left and right and up and down:
            if lastMove == "left":
                move("up")
                continue
            if lastMove == "right":
                move("down")
                continue
            if lastMove == "up":
                move("right")
                continue
            if lastMove == "down":
                move("left")
                continue
            move("down", False)
            continue
        else:
            if lastMove == "left" and not left:
                if down:
                    move("down")
                    continue
                else:
                    move("up")
                    continue
            if lastMove == "right" and not right:
                if up:
                    move("up")
                    continue
                else:
                    move("down")
                    continue
            if lastMove == "up" and not up:
                if left:
                    move("left")
                    continue
                else:
                    move("right")
                    continue
            if (lastMove == "down" or lastMove == None) and not down:
                if right:
                    move("right")
                    continue
                else:
                    move("left")
                    continue
        move(lastMove)


def move(s, setLM=True):
    global lastMove
    
    if setLM == True:
        lastMove = s 

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


def positionChanged(vm):
    observations = cave.observe(vm)
    return xPos != observations.myX or yPos != observations.myY

def waitToLoad(t):
    for _ in range(t):
        vm.act(cave.actions.none)

start()