import chipgr8
import chipgr8.games as games
import random
import timeit

# Choose a gamee with a `score` and `done` observation
game = games.Squash

# Initialize 100 instances of the game
vms = chipgr8.init(instances=100, ROM=game.ROM, sampleRate=12)

def action(vm):
    vm.act(random.choice(game.actions)) # Choose a random action
    vm.doneIf(game.observe(vm).done)    # Mark done if done

# Run all the vms in parrallel
vms.inParallel(action)

# Select the best by score
best = vms.maxBy(lambda vm : game.observe(vm).score)

# Print the inputHistory so it can be saved
print(best.inputHistory)
# Show the game
chipgr8.init(
    display      = True, 
    ROM          = game.ROM,
    inputHistory = best.inputHistory,
).go()