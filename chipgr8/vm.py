import os
import pygame
import pickle as pkl
import numpy  as np

import chipgr8.io           as io
import chipgr8.core         as core
import chipgr8.shaders      as shaders
import chipgr8.disassembler as disassembler

from chipgr8.util import write, findROM
from lazyarray    import larray

class Chip8VM(object):
    '''
    Wraps the Chip8VMStruct object produced by core.initVM, provides a 
    pythonic interface to the VM state, and performs IO actions if necessary.
    '''

    __freq = 600
    '''The VM runnning frequency'''

    __pausedFreq = 30
    '''The VM paused frequency'''

    __VMs = None
    '''Containing VM collection'''

    ROM = None
    '''The ROM file path'''

    VM = None
    '''The VM struct instance'''

    ctx = None
    '''Lazy array (numpy compliant) repesenting video memory'''

    inputHistory = []
    '''All input events a list of tuples (key, steps)'''

    sampleRate = 1
    '''For AI agents, how many steps are taken per act'''

    stepCounter = 0
    '''How many steps were taken since the last sample'''

    aiKeys = 0
    '''Input last pressed by the AI agent'''

    smooth = False
    '''Flag for smooth rendering'''
    
    paused = False
    '''Flag for pausing'''

    window = None
    '''Window instance'''

    keys = 0
    '''Current input keys sample'''

    done = False
    '''Indicates whether the VM is in a done state'''

    def __init__(
        self,
        ROM          = None,
        frequency    = 600,
        loadState    = None,
        inputHistory = None,
        sampleRate   = 1,
        display      = False,
        smooth       = False,
        startPaused  = False,
        shader       = shaders.default,
    ):
        '''
        Initializes a new Chip8VM object. Responsible for allocating a new VM
        struct, game window, etc. If called with display equal to true will
        begin the game loop.

        @params ROM             str                name or path to the ROM to load
                frequency       int                frequency to run the VM at
                loadState       str                path or tag to a save state
                inputHistory    List[(int, int)]   a list of predifined IO events
                sampleRate      int                how many steps act moves forward
                display         bool               if true creates a game window
                smooth          bool               if true uses smooth rendering
                startPaused     bool               if true starts the vm paused
                shader          Shader             display shader to use
        '''
        # TODO adjust for Super Chip-48
        width, height = 64, 32

        self.__freq = (frequency // 60) * 60
        self.smooth = smooth
        self.paused = startPaused
        self.window = io.ChipGr8Window(width, height) if display else None
        self.VM     = core.initVM(frequency // 60)
        self.loadROM(ROM)

        def getVRAM(x, y):
            bit        = (y * width) + x
            byteOffset = bit // 8
            bitOffset  = bit %  8
            byte       = self.VM.VRAM[byteOffset]
            return (byte >> (7 - bitOffset)) & 0x1
        
        self.ctx    = larray(getVRAM, shape=(width, height))

    def __del__(self):
        '''
        Releases VM resources
        '''
        core.freeVM(self.VM)

    # ROM Methods

    def go(self, function=None, aiInputMask=None, actBetweenSamples=True):
        '''
        Runs displayable VM core loop.

        @params function            The AI agent function. May return a 16-bit integer representing intended keypresses
                aiInputMask         A mask for combining user and AI inputs. If None, inputs will be logically ORed. If
                                    any 16-bit integer, inputs made by the AI for keys masked with 0 will be ignored.
                                    Inputs made by a user for keys masked with 1 will also be ignored.
                actBetweenSamples   If true, keys pressed by the AI will remain pressed until the next sample
        '''
        assert self.window, 'Cannot start a VM with no window!'
        assert self.ROM,    'Cannot start a VM with no ROM!'

        clk = pygame.time.Clock()
        
        self.window.initDisassemblyText(self.ROM.encode())
        self.window.clear()
        self.render(forceDissassemblyRender=True)

        while (self.eventProcessor()):
            if self.paused:
                clk.tick(self.__pausedFreq)
            else:
                # Add masked user input to combined input
                combinedInput = self.keys if aiInputMask is None else self.keys & ~aiInputMask
                if function:
                    # Get masked ai input when AI step is occuring. Otherwise, apply last move if enabled
                    if self.stepCounter == 0:
                        self.aiKeys = function()
                    if self.stepCounter == 0 or actBetweenSamples:
                        combinedInput |= self.aiKeys if aiInputMask is None else self.aiKeys & aiInputMask
                self.input(combinedInput)
                # Update AI step counter
                self.stepCounter = (self.stepCounter + 1) % self.sampleRate

                clk.tick(self.__freq)
                self.step()
            self.render(pcHighlight=self.paused)

    def loadROM(self, nameOrPath):
        '''
        Load a ROM from the given path, or check if it is the name of a ROM in
        `data/roms`. Throws an error if no ROM could be found. Internally calls
        core.loadROM.

        @params nameOrPath The name or path of the ROM to load
        '''
        if self.VM == None:
            raise RuntimeError("VM not loaded.")

        self.ROM = findROM(nameOrPath)

        if not self.ROM:
            raise FileNotFoundError("The specified file does not exist.")
        if not core.loadROM(self.VM, self.ROM.encode()):
            raise RuntimeError("Library failed to load ROM.")
    
    # State Methods

    def loadState(self, path=None, tag=None):
        '''
        Load state from a file or from a tag. Tagged states are stored in 
        `data/tags`. If no file can be provided throws an error.

        @params path If provided, the path to load the state from
                tag  If provided, the tag of the state
        '''
        #TODO: What are tags

        if not os.path.isfile(path):
            raise FileNotFoundError("Save state file not found.")
        
        self.VM = pkl.load(open(path, 'rb'))

    def saveState(self, path=None, tag=None, force=False):
        '''
        Save state to a file or to a tag (ie. `data/tags/<tag>`).
        
        @params path  If provided, the path to save the state to
                tag   If provided, the tag to save the state to
                force If true, overwrite already existing files, otherwise
                      throw an error
        '''
        #TODO: What are tags

        if not os.path.isfile(path) or force:
            pkl.dump(self.VM, open(path, 'bw'))
        else:
            raise FileExistsError("File already exists.")

    # IO Methods

    def input(self, keys):
        '''
        Set the current VM IO state.

        @params keys    int     
                A raw set of bytes representing the io memory
        '''
        core.sendInput(self.VM, keys)

    def render(self, forceDissassemblyRender=False, pcHighlight=False):
        '''
        Force a render to the window (if it is open).
        '''
        if self.window:
            if self.VM.diffClear:
                self.window.clear()
            if self.smooth:
                if self.VM.diffSize and not self.VM.diffSkip:
                    self.window.fullRender(self.ctx)
            else:
                if self.VM.diffSize:
                    self.window.render(
                        self.ctx, 
                        self.VM.diffX, 
                        self.VM.diffY, 
                        self.VM.diffSize,
                    )
                
            self.window.renderDisassembly(override=forceDissassemblyRender, highlight=pcHighlight)
            self.window.sound(self.VM.ST[0] > 0)
    
    # State Methods

    def step(self):
        '''
        Simulate a single VM clock cycle. Internally calls core.step.
        '''
        core.step(self.VM)

    def steps(self, n):
        '''
        Simulate a number of clock cycles in a row. Internally calls core.step.
        '''
        while n > 0:
            core.step(self.VM)
            n -= 1

    def reset(self):
        '''
        Complete reset to original state. Reloads ROM.
        '''
        pass # TODO

    def linkVMs(self, VMs):
        '''
        Links VM with a VM collection.

        @param VMs  Chip8VMs     the collection to link to
        '''
        self.__VMs = VMs

    def act(self, action):
        '''
        Performs an action and steps forward.
        
        @param action   int     input action to perform
        '''
        self.input(action)
        self.steps(self.sampleRate)

    def doneIf(self, done):
        '''
        Sets the VM to done if `done` is true. Signals VMs collection if 
        applicable.

        @param done     bool    if done
        '''
        if not self.done and done:
            self.done = True
            if self.__VMs:
                self.__VMs.signalDone(self)

    # Event Processor

    def eventProcessor(self):
        if self.VM is None:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.window: # TODO: Disassembly scrolling speed currently limited by framerate unless paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scrollDisassemblyUp(numLines=2)
                    elif event.button == 5:
                        self.scrollDisassemblyDown(numLines=2)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.togglePause()
                    if event.key == pygame.K_F6 and self.paused:
                        self.step()
                        self.highlightDisassembly()
                    if event.key == pygame.K_PAGEUP:
                        self.scrollDisassemblyUp(numLines=4)
                    if event.key == pygame.K_PAGEDOWN:
                        self.scrollDisassemblyDown(numLines=4)
                    if event.key == pygame.K_HOME:
                        self.scrollDisassemblyUp()
                    if event.key == pygame.K_END:
                        self.scrollDisassemblyDown()

                self.keyProcessor(event)

        return True

    def keyProcessor(self, event):
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

    # UI Actions

    def togglePause(self):
        self.paused = not self.paused
        self.highlightDisassembly()

    def scrollDisassemblyUp(self, numLines=None):
        if self.window:
            if numLines == None:
                self.window.scrollDissassemblyToLine(0)
            else:
                self.window.offsetScrollDisassembly(-1 * numLines)

    def scrollDisassemblyDown(self, numLines=None):
        if self.window:
            if numLines == None:
                self.window.scrollDissassemblyToLine(self.window.getLastDisassemblyLine(), centre=False)
            else:
                self.window.offsetScrollDisassembly(numLines)

    def highlightDisassembly(self):
        if self.window:
            self.window.setWarningStatus(core.getProgramCounter(self.VM) % 2 == 1)
            line = (core.getProgramCounter(self.VM) - 512) // 2 + 1 # Offset interpret space and add 1 because 1-indexing
            self.window.setCurrDisassemblyLine(line)
            self.window.scrollDissassemblyToCurrLine()