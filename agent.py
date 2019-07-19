import chipgr8
import chipgr8.games.pong as Pong
import random
import pickle as pkl
import numpy as np
from sklearn.neural_network import MLPClassifier as classifier

#agent = classifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(265,265), random_state=1)
agent = classifier(solver='sgd', alpha=1e-5, random_state=1)

fitted = False

while True:

    pong = Pong.pong
    # Creates 100 instances of pong
    #vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)
    vm = chipgr8.init(display=false, ROM=pong.ROM, instances=100)

    # Plays 100 games of pong until all games are finished
    ram = []
    history = [] 
    best = 0
    last = 0
    score = 0

    first = True

    while not vm.done:

        # Retrieves relevant data from memory
        observations = pong.observer(vm)#.observe(vm)

        if not fitted:
            # Selects a valid key for pong
            action = random.choice(pong.actions)
        else:
            action = agent.predict(np.array(vm.VM.RAM).reshape(1, -1))

        history.append(action)
        ram.append(vm.VM.RAM)
        score = observations.score

        if observations.score > best or (not first and len(ram) > last):
            fitted = True
            agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2,16])
            with open("my_agent.pkl", 'wb') as f:
                pkl.dump(agent, f)

        # Performs the selected key
        vm.act(action)

        # Determines if the game of pong has ended
        vm.doneIf(observations.done)

    if first:
        first = False

    if len(ram) > last: 
        last = len(ram)

    if score > best:
        best = score


    #if not fitted:
    #    fitted = True
    #    with open("agent.pkl", 'wb') as f:
    #        agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2, 16])
    #        pkl.dump(agent, f)
            

