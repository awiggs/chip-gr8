from chipgr8.vm      import Chip8VM
from time            import sleep

import pygame
import chipgr8.core    as core
import chipgr8.shaders as shaders

class ChipGr8(object):
    pauseFreq = 1000
    currFreq = pauseFreq
    gamePaused = False
    vm = None

    def __init__(
        self,
        verbose      = False,
        smooth       = False,
        display      = False,
        frequency    = 500,
        loadState    = None,
        ROM          = None,
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

        self.vm = Chip8VM(frequency=frequency, smooth=smooth, display=display)
        
        # self.vm.window.shader = shaders.rainbow
        # self.vm.window.background = (255, 255, 255)

        # self.vm.window.foreground = (0, 0, 0)
        # self.vm.window.background = (255, 255, 255)

        self.vm.window.clear()

        if ROM is not None:
            print('Loading ROM: "{}"...'.format(ROM))
            self.vm.loadROM(ROM)

        clk = pygame.time.Clock()
        self.currFreq = self.vm.freq

        self.vm.render(forceDissassemblyRender=True)

        while(self.eventProcessor()):
            clk.tick(self.currFreq)
            if not self.gamePaused:
                self.vm.step()
            self.vm.render(pcHighlight=self.gamePaused)

        # Cleanup
        core.freeVM(self.vm.vm)
        print('Finished.')

    def eventProcessor(self):
        if self.vm is None:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.vm.window: # TODO: Disassembly scrolling speed currently limited by framerate unless paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.vm.window.scrollDisassemblyUp()
                    elif event.button == 5:
                        self.vm.window.scrollDisassemblyDown()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.togglePause()
                    elif event.key == pygame.K_F6 and self.gamePaused:
                        self.vm.step()
                        self.vm.highlightDisassembly()

        return True

    def togglePause(self):
        self.gamePaused = not self.gamePaused
        self.currFreq = self.pauseFreq if self.gamePaused else self.vm.freq
        self.vm.highlightDisassembly()