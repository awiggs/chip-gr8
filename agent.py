import chipgr8
import chipgr8.games.pong as Pong
import random
import pickle as pkl
import numpy as np
from sklearn.neural_network import MLPClassifier as classifier

#agent = classifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(265,265), random_state=1)

agent = classifier(solver='sgd', alpha=1e-5, random_state=1)
pong = Pong.pong
INSTANCES = 100

vms = chipgr8.init(display=False, ROM=pong.ROM, instances=INSTANCES)

agents = [ classifier(solver='sgd', alpha=1e-5, random_state=1) for _ in range(100) ]

while vms.done:
    for i, vm in vms.items():
        observations = pong.observer(vm)

        action = random.choice(pong.actions)

        if observations.score > 0:
            agents[i].partial_fit(np.array(ram), np.array(history), classes=[0, 2,16])
            with open("multi{0}.pkl".format(i), 'wb') as f:
                pkl.dump(agent, f)

        # Performs the selected key
        vm.act(action)

        # Determines if the game of pong has ended
        vm.doneIf(observations.done)
