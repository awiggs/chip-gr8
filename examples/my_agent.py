import chipgr8
import chipgr8.games.pong as Pong
import random

pong = Pong.pong
# Creates 100 instances of pong
vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)

# Plays 100 games of pong until all games are finished
while not vm.done:
   #for vm in vms:
   # Retrieves relevant data from memory
   observations = pong.observer(vm)#.observe(vm)
   # Selects a valid key for pong
   action       = random.choice(pong.actions)
   # Performs the selected key
   vm.act(action)
   # Determines if the game of pong has ended
   vm.doneIf(observations.done)

# Determines best vm by score
#best = vms.maxBy(lambda vm : pong.observer(vm).score)
#best = vms.get()[0]
# Creates a replay that opens a display the user can play/pause/step
#vm = chipgr8.init(
#   ROM=pong.ROM,
#   inputHistory=best.inputHistory,
#   display=True
#).go()
