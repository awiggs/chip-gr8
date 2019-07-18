import os, sys
sys.path.append(os.path.expanduser('C:/Users/jonbe/Desktop/SENG499/chip-gr8'))
import chipgr8
import chipgr8.games.cave as Cave

# Constants
rate = 100

cave = Cave.cave
vm = chipgr8.init(display=True, ROM=cave.ROM, sampleRate=rate)

# wait for the game to finish loading
for _ in range(10):
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
    up      = vm.ctx[xPos, yPos - 1]
    right   = vm.ctx[xPos + 1, yPos]
    down    = vm.ctx[xPos, yPos + 1]
    left    = vm.ctx[xPos - 1, yPos]
    
    # make a decision
    if right == 0:
        vm.act(cave.actions.right)  # move right
        continue
    if up == 0:
        vm.act(cave.actions.up)     # move up
        continue
    if down == 0:
        vm.act(cave.actions.down)   # move down
        continue
    if left == 0:
        vm.act(cave.actions.left)   # move left