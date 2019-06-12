from chipgr8.vm   import Chip8VM
from chipgr8.core import freeVM
from time         import sleep

import pygame

def init(
    verbosity    = False,
    loadState    = None,
    ROM          = None,
    display      = None,
    timing       = None,
    memoryTables = None,
    instances    = None,
    # Additional options
):
    '''
    Initializes the chipgr8 library and returns a new instance of Chip8VM from
    `chipgr8/vm.py`, providing that object the appropriate options. Multiple 
    instances may also be provided.

    @params loadState    A path to a save state to load
            ROM          A ROM to load
            display      If true a window will display the VM display
            timing       The timing convention used when step is called
            memoryTables A method of specifying ROM specific fields
    @returns             The VM instance or instances
    '''
    if display:
        display = True
    else:
        display = False

    vm = Chip8VM(display=display)
    if ROM is not None:
        vm.loadROM(ROM)

    clk = pygame.time.Clock()

    while(eventProcessor()):
        clk.tick(240)
        vm.step()
        vm.render()

    # Cleanup
    freeVM(vm.vm)
    print('Finished.')

def eventProcessor():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

