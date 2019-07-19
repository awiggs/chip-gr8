import chipgr8
import chipgr8.games.pong as Pong
import random
import pickle as pkl
import numpy as np
from sklearn.neural_network import MLPClassifier as classifier

vms = chipgr8.init(display=False, ROM=Pong.pong.ROM, instances=100)
agent = classifier(solver='sgd', alpha=1e-5, random_state=1)

print("what")
DONE = False
while not DONE:
    for i, vm in enumerate(vms):
        # Retrieves relevant data from memory
        observations = pong.observer(vm)

        action = random.choice(pong.actions)

        #if observations.score > best or (not first and len(ram) > last):
        #    fitted = True
        #    agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2,16])
        #    with open("my_agent.pkl", 'wb') as f:
        #        pkl.dump(agent, f)

        # Performs the selected key
        vm.act(action)

        if observations.done:
            with open("my_agent({0}).pkl".format(i), 'wb') as f:
                pkl.dump(agent, f)


        # Determines if the game of pong has ended
        vm.doneIf(observations.done)

bettest = vms.maxBy(lambda vm: pong.observer(vm).score)

agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2,16])
# Creates a replay that opens a display the user can play/pause/step
vm = chipgr8.init(
   ROM=Pong.pong.ROM,
   inputHistory=bestest.inputHistory,
   display=True).go()


    
