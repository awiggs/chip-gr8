import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
import chipgr8.games.cave as Cave

# Globals
rate = 1
touching = [False,False,False,False]
lastTouch = [False, False, False, False]

cave = Cave.cave
vm = chipgr8.init(display=True, ROM=cave.ROM, sampleRate=rate)

# wait for the game to finish loading
for _ in range(1000):
    vm.act(0)

# start the game
vm.act(cave.actions.start)

#loop actions
while not vm.done:

    # get new observations (x,y) position
    observations = cave.observer(vm)
    xPos = observations.myX
    yPos = observations.myY

    # get the value of my up,down,left,right
    try:
        touching[0] = vm.ctx()[xPos, yPos - 1] == 0 # up is safe
        touching[1] = vm.ctx()[xPos + 1, yPos] == 0 # right is safe
        touching[2] = vm.ctx()[xPos, yPos + 1] == 0 # down is safe
        touching[3] = vm.ctx()[xPos - 1, yPos] == 0 # left is safe
    except:
        vm.act(cave.actions.right)
    
    # Make decisions
    

    vm.act(0)