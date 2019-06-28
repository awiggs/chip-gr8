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
    keys = 0

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
            self.vm.input(self.keys)
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
                        self.vm.scrollDisassemblyUp(numLines=2)
                    elif event.button == 5:
                        self.vm.scrollDisassemblyDown(numLines=2)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.togglePause()
                    if event.key == pygame.K_F6 and self.gamePaused:
                        self.vm.step()
                        self.vm.highlightDisassembly()
                    if event.key == pygame.K_PAGEUP:
                        self.vm.scrollDisassemblyUp(numLines=4)
                    if event.key == pygame.K_PAGEDOWN:
                        self.vm.scrollDisassemblyDown(numLines=4)
                    if event.key == pygame.K_HOME:
                        self.vm.scrollDisassemblyUp()
                    if event.key == pygame.K_END:
                        self.vm.scrollDisassemblyDown()

                self.checkInputKeys(event)

        return True

    def togglePause(self):
        self.gamePaused = not self.gamePaused
        self.currFreq = self.pauseFreq if self.gamePaused else self.vm.freq
        self.vm.highlightDisassembly()

    def checkInputKeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                self.keys |= 1
            if event.key == pygame.K_1:
                self.keys |= 1 << 1
            if event.key == pygame.K_2:
                self.keys |= 1 << 2
            if event.key == pygame.K_3:
                self.keys |= 1 << 3
            if event.key == pygame.K_4:
                self.keys |= 1 << 4
            if event.key == pygame.K_5:
                self.keys |= 1 << 5
            if event.key == pygame.K_6:
                self.keys |= 1 << 6
            if event.key == pygame.K_7:
                self.keys |= 1 << 7
            if event.key == pygame.K_8:
                self.keys |= 1 << 8
            if event.key == pygame.K_9:
                self.keys |= 1 << 9
            if event.key == pygame.K_a:
                self.keys |= 1 << 10
            if event.key == pygame.K_b:
                self.keys |= 1 << 11
            if event.key == pygame.K_c:
                self.keys |= 1 << 12
            if event.key == pygame.K_d:
                self.keys |= 1 << 13
            if event.key == pygame.K_e:
                self.keys |= 1 << 14
            if event.key == pygame.K_f:
                self.keys |= 1 << 15
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_0:
                self.keys &= ~(1)
            if event.key == pygame.K_1:
                self.keys &= ~(1 << 1)
            if event.key == pygame.K_2:
                self.keys &= ~(1 << 2)
            if event.key == pygame.K_3:
                self.keys &= ~(1 << 3)
            if event.key == pygame.K_4:
                self.keys &= ~(1 << 4)
            if event.key == pygame.K_5:
                self.keys &= ~(1 << 5)
            if event.key == pygame.K_6:
                self.keys &= ~(1 << 6)
            if event.key == pygame.K_7:
                self.keys &= ~(1 << 7)
            if event.key == pygame.K_8:
                self.keys &= ~(1 << 8)
            if event.key == pygame.K_9:
                self.keys &= ~(1 << 9)
            if event.key == pygame.K_a:
                self.keys &= ~(1 << 10)
            if event.key == pygame.K_b:
                self.keys &= ~(1 << 11)
            if event.key == pygame.K_c:
                self.keys &= ~(1 << 12)
            if event.key == pygame.K_d:
                self.keys &= ~(1 << 13)
            if event.key == pygame.K_e:
                self.keys &= ~(1 << 14)
            if event.key == pygame.K_f:
                self.keys &= ~(1 << 15)