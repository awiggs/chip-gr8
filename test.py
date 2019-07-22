import chipgr8
import random

from chipgr8.games import Pong1Player

vms = chipgr8.init(
    instances  = 2,
    ROM        = Pong1Player.ROM,
    sampleRate = 12,
)

def action(vm):
    obs = Pong1Player.observe(vm)
    vm.act(random.choice(Pong1Player.actions))
    vm.doneIf(obs.done)

while not vms.done():
    for vm in vms:
        action(vm)

    # vms.inParallel(action)

best = vms.maxBy(lambda vm : Pong1Player.observe(vm).score)

chipgr8.init(
    display      = True, 
    ROM          = Pong1Player.ROM,
    inputHistory = best.inputHistory,
).go()