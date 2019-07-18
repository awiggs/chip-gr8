import chipgr8
import chipgr8.games.pong as Pong
import random
import numpy as np
from agent import agent

pong = Pong.pong
# Creates 100 instances of pong
vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)

# Plays 100 games of pong until all games are finished
while not vm.done:

   # Retrieves relevant data from memory
   observations = pong.observer(vm)#.observe(vm)

   # Selects a valid key for pong
   #action       = random.choice(pong.actions)
   #print("{},{},{},{}".format(observations.score, observations.opponent, action))
   X = np.array([observations.score, observations.opponent]).reshape(1, -1)
   #Y.append([ 1 if action == 16 or 2 else 0, 1 if action == 16 or 12 else 0])
   #X.append([action])
   pred = agent.predict(X) 
   action = 2 if pred[0][0] == 1 else 16
   #print((pred[0][0], pred[0][1]))

   # Performs the selected key
   vm.act(action)

   # Determines if the game of pong has ended
   vm.doneIf(observations.done)
#print("X=================")
#print(vm.inputHistory)
#print("Y=================")
#print(observations.score)
#print(observations.opponent)
# Determines best vm by score
#best = vms.maxBy(lambda vm : pong.observer(vm).score)
#best = vms.get()[0]
# Creates a replay that opens a display the user can play/pause/step
#vm = chipgr8.init(
#   ROM=pong.ROM,
#   inputHistory=best.inputHistory,
#   display=True
#).go()

