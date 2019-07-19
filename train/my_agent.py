import chipgr8
import chipgr8.games.pong as Pong
import random
import pickle as pkl
import numpy as np
from sklearn.neural_network import MLPClassifier as classifier

#agent = classifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(265,265), random_state=1)
agent = classifier(solver='sgd', alpha=1e-5, random_state=1)

pong = Pong.pong
# Creates 100 instances of pong
vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)

# Plays 100 games of pong until all games are finished
X = []
Y = []
fitted = False
ram = []
history = [] 
while not vm.done:

    # Retrieves relevant data from memory
    observations = pong.observer(vm)#.observe(vm)

    if not fitted:
        # Selects a valid key for pong
        action       = random.choice(pong.actions)

    #diff = observations.score - observations.opponent

    if (observations.score > 0 and not fitted):
        fitted = True
        agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2,16])
        with open("my_agent.pkl", 'wb') as f:
            pkl.dump(agent, f)

    # Performs the selected key
    vm.act(action)
    
    #res = 0
    #for i,r in enumerate(vm.VM.RAM):
    #    res += int(i) << i

    ram.append(vm.VM.RAM)
    history.append(action)
    # Determines if the game of pong has ended
    vm.doneIf(observations.done)

if not fitted:
    with open("my_agent.pkl", 'wb') as f:
        ram = np.array(ram)
        history = np.array(history)
        print(ram.shape)
        print(history.shape)
        print(ram)
        print(history)
        agent.partial_fit(ram, history, classes=[0, 2,16])
        pkl.dump(agent, f)
        

