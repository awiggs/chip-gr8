from chipgr8.vm      import Chip8VM
from time            import sleep

import pygame
import chipgr8.core    as core
import chipgr8.shaders as shaders

def init(
    verbose      = False,
    smooth       = False,
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

    vm = Chip8VM(smooth=smooth, display=display)
    
    # vm.window.shader = shaders.rainbow
    # vm.window.background = (255, 255, 255)

    # vm.window.foreground = (0, 0, 0)
    # vm.window.background = (255, 255, 255)

    vm.window.clear()

    if ROM is not None:
        print('Loading ROM: "{}"...'.format(ROM))
        vm.loadROM(ROM)

    clk = pygame.time.Clock()

    while(eventProcessor()):
        clk.tick(240)
        vm.step()
        vm.render()

    # Cleanup
    core.freeVM(vm.vm)
    print('Finished.')

def eventProcessor():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

