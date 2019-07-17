import os
import sys
import json
import pygame
import pickle as pkl

import chipgr8.core    as core
import chipgr8.shaders as shaders

from chipgr8.window import Window
from chipgr8.util   import write, findROM
from lazyarray      import larray
from collections    import namedtuple

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

    smooth = False
    '''Flag for smooth rendering'''
    
    paused = False
    '''Flag for pausing'''

    record = True
    '''Flag for recording input history'''

    inputHistory = []
    '''All input events a list of tuples (key, steps)'''

    sampleRate = 1
    '''For AI agents, how many steps are taken per act'''

    window = None
    '''Window instance'''

    userKeys = 0
    '''Current input keys sample'''

    aiKeys = 0
    '''Input last pressed by the AI agent'''

    aiInputMask = 0
    '''Input mask to combine user and AI input'''

    done = False
    '''Indicates whether the VM is in a done state'''

    pyclock = None
    '''Pygame clock'''


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
        aiInputMask  = 0,
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
                aiInputMask     int                A mask for combining user and AI inputs. If
                                                   any 16-bit integer, inputs made by the AI for
                                                   keys masked with 0 will be ignored. Inputs made
                                                   by a user for keys masked with 1 will also be ignored.
        '''
        assert inputHistory is None or len(inputHistory) > 1, 'Input history mut have recorded at least two key presses!'

        self.record       = inputHistory is None
        self.inputHistory = inputHistory or [(0, 0)]
        self.aiInputMask  = aiInputMask
        self.historyPos   = 0
        self.__freq       = (frequency // 60) * 60
        self.smooth       = smooth
        self.paused       = startPaused
        self.VM           = core.initVM(frequency // 60)
        self.loadROM(ROM)

        width, height = 64, 32
        def getVRAM(x, y):
            bit        = (y * width) + x
            byteOffset = bit // 8
            bitOffset  = bit %  8
            byte       = self.VM.VRAM[byteOffset]
            return (byte >> (7 - bitOffset)) & 0x1
        
        self.ctx     = larray(getVRAM, shape=(width, height))
        self.window  = Window(width, height) if display else None
        self.pyclock = pygame.time.Clock()   if display else None        

    def __del__(self):
        '''
        Releases VM resources
        '''
        core.freeVM(self.VM)

    def go(self):
        '''
        Runs displayable VM core loop.

        @params function            The AI agent function
        '''
        assert self.window, 'Cannot start a VM with no window!'
        assert self.ROM,    'Cannot start a VM with no ROM!'

        try:
            while not self.done:
                self.act(0)
        except KeyboardInterrupt:
            print('Goodbye!')

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

    def input(self, keys, user=False):
        '''
        Set the current VM IO state.

        @params keys    int     
                A raw set of bytes representing the io memory
        '''
        if user:
            self.userKeys = keys
        else:
            self.aiKeys = keys
        core.sendInput(self.VM, (self.aiKeys & self.aiInputMask) | (self.userKeys & ~self.aiInputMask))
    
    def step(self):
        '''
        Simulate a single VM clock cycle. Internally calls core.step.
        '''
        keys = self.VM.keys[0]
        if self.record and keys != self.inputHistory[-1][0]:
            self.inputHistory.append((keys, self.VM.clock))
        if not self.record and not self.done:
            # Use the previous input until the next stored change is encountered
            if self.VM.clock < self.inputHistory[historyPos + 1][1]:
                self.input(self.inputHistory[self.historyPos][0])
            else:
                historyPos += 1
                self.doneIf(self.historyPos + 1 == len(self.inputHistory))
                self.input(self.inputHistory[self.historyPos][0])
        core.step(self.VM)
        self.aiKeys   = 0
        self.userKeys = 0

    def reset(self):
        '''
        Complete reset to original state. Reloads ROM.
        '''
        self.VM = core.initVM(self.__freq // 60)
        loadROM(self.ROM)

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
        for _ in range(self.sampleRate):
            if not self.paused:
                self.input(action)
                self.step()
            if self.window:
                self.window.update(self)
                self.window.render(force=self.paused)
                self.pyclock.tick(self.__pausedFreq if self.paused else self.__freq)

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
