import chipgr8
import chipgr8.games.pong as Pong
import random
import pickle as pkl
import numpy as np
#import stats

from sklearn.neural_network import MLPClassifier as classifier
#agent = classifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)

#agent = classifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(265,265), random_state=1)

while True:
    agent = None
    with open("my_agent2.pkl", 'rb') as f:
        agent = pkl.load(f)

    pong = Pong.pong
    # Creates 100 instances of pong
    vm = chipgr8.init(display=True, ROM=pong.ROM, instances=1)

    ram = []
    history = [] 
    last = 0
    best = 0
    first = True
    while not vm.done:

        ram.append(vm.VM.RAM)

        # Retrieves relevant data from memory
        observations = pong.observer(vm)#.observe(vm)

        action = agent.predict(np.array(vm.VM.RAM).reshape(1, -1))
        history.append(action)

        if (observations.score > best):
            best = observations.score
            print("TRAINING==============================================")
            agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2, 16])
            with open("my_agent2.pkl", 'wb') as f:
                pkl.dump(agent, f)
            print("DONE WRITING==========================================")


        # Performs the selected key
        vm.act(action)
        
        # Determines if the game of pong has ended
        if observations.done:
            if first: 
                first = False
                last = len(ram)
            if len(ram) > last:
                last = len(ram)
                print("TRAINING==============================================")
                agent.partial_fit(np.array(ram), np.array(history), classes=[0, 2, 16])
                with open("my_agent2.pkl", 'wb') as f:
                    pkl.dump(agent, f)
                print("DONE WRITING==========================================")

        vm.doneIf(observations.done)
