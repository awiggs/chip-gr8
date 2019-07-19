import os
import sys
import json
import pygame
import pickle
import logging

import chipgr8.core as core

from chipgr8.window import Window
from chipgr8.util   import write, findROM, resolveTag
from lazyarray      import larray
from collections    import namedtuple

logger = logging.getLogger(__name__)

class Chip8VM(object):
    '''
    Wraps the Chip8VMStruct object produced by core.initVM, provides a 
    pythonic interface to the VM state, and performs IO actions if necessary.
    '''

    

    __pausedFreq = 30
    '''The VM paused frequency'''

    __VMs = None
    '''Containing VM collection'''

    __ctx = None
    '''Graphics content cache'''

    __freq = 600
    '''The VM runnning frequency'''

    window = None
    '''Window instance'''

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

    historyPos = 0
    '''Index of history for playback'''

    inputHistory = []
    '''All input events a list of tuples (key, steps)'''

    sampleRate = 1
    '''For AI agents, how many steps are taken per act'''

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
        ROM,
        frequency,
        loadState,
        inputHistory,
        sampleRate,
        display,
        smooth,
        startPaused,
        aiInputMask,
        foreground,
        background,
        unpausedDisScroll,
    ):
        '''
        Initializes a new Chip8VM object. Responsible for allocating a new VM
        struct, game window, etc. If called with display equal to true will
        begin the game loop.

        @params ROM             str              name or path to the ROM to load
                frequency       int              frequency to run the VM at
                loadState       str              path or tag to a save state
                inputHistory    List[(int, int)] a list of predifined IO events
                sampleRate      int              how many steps act moves forward
                display         bool             if true creates a game window
                smooth          bool             if true uses smooth rendering
                startPaused     bool             if true starts the vm paused
                shader          Shader           display shader to use
                aiInputMask     int              A mask for combining user and AI inputs. If
                                                 any 16-bit integer, inputs made by the AI for
                                                 keys masked with 0 will be ignored. Inputs made
                                                 by a user for keys masked with 1 will also be ignored.
                foreground      (int, int, int)  hex color code or color tuple
                background      (int, int, int)  hex color code or color tuple
        '''
        assert inputHistory is None or len(inputHistory) > 1, 'Input history mut have recorded at least two key presses!'

        self.sampleRate   = sampleRate
        self.record       = inputHistory is None
        self.inputHistory = inputHistory or [(0, 0)]
        self.aiInputMask  = aiInputMask
        self.historyPos   = 0
        self.__freq       = (frequency // 60) * 60
        self.smooth       = smooth
        self.paused       = startPaused
        self.VM           = core.initVM(frequency // 60)
        if ROM:
            self.loadROM(ROM, reset=False)
        self.window = Window(
            64, 32, 
            foreground = foreground, 
            background = background,
            scrollDisOnUpdate=unpausedDisScroll
        ) if display else None
        self.pyclock = pygame.time.Clock() if display else None

    def ctx(self):
        if not self.__ctx:
            width, height = 64, 32
            def getVRAM(x, y):
                bit        = (y * width) + x
                byteOffset = bit // 8
                bitOffset  = bit %  8
                byte       = self.VM.VRAM[byteOffset % 0x100]
                return (byte >> (7 - bitOffset)) & 0x1
            self.__ctx = larray(getVRAM, shape=(width, height))
        return self.__ctx

    def clearCtx(self):
        self.__ctx = None

    def go(self):
        '''
        Runs displayable VM core loop.

        @params function            The AI agent function
        '''
        assert self.window, 'Cannot use `go` without a window'
        logger.info('VM starting in user mode (go) `{}`'.format(self))
        try:
            while not self.done:
                self.act(0)
        except KeyboardInterrupt:
            print('Goodbye!')

    def loadROM(self, nameOrPath, reset=True):
        '''
        Load a ROM from the given path, or check if it is the name of a ROM in
        `data/roms`. Throws an error if no ROM could be found. Internally calls
        core.loadROM.

        @params nameOrPath The name or path of the ROM to load
        '''
        logger.info('Loading rom `{}` into `{}`'.format(nameOrPath, self))
        if reset:
            self.reset()
        self.ROM = findROM(nameOrPath)
        if not self.ROM:
            raise FileNotFoundError("ROM `{}` does not exist.".format(self.ROM))
        if not core.loadROM(self.VM, self.ROM.encode()):
            raise RuntimeError("Library failed to load ROM.")
        if self.window:
            self.window.refresh(self)
        return 'Loaded ROM.'
    
    def loadState(self, path=None, tag=None):
        '''
        Load state from a file or from a tag. Tagged states are stored in 
        `data/tags`. If no file can be provided throws an error.

        @params path If provided, the path to load the state from
                tag  If provided, the tag of the state
        '''
        assert path or tag
        logger.info('Loading state from `{}` into `{}`'.format(path or tag, self))
        if tag:
            path = resolveTag(tag)
        if not os.path.isfile(path):
            raise FileNotFoundError("Save state file not found.")
        self.VM = pickle.load(open(path, 'rb'))
        if self.window:
            self.window.refresh(self)
        return 'Save state loaded.'

    def saveState(self, path=None, tag=None, force=False):
        '''
        Save state to a file or to a tag (ie. `data/tags/<tag>`).
        
        @params path  If provided, the path to save the state to
                tag   If provided, the tag to save the state to
                force If true, overwrite already existing files, otherwise
                      throw an error
        '''
        assert path or tag
        logger.info('Saving state to `{}` for `{}`'.format(path or tag, self))
        if tag:
            path = resolveTag(tag)
        print('> ', os.path.exists(path))
        if not os.path.exists(path) or force:
            pickle.dump(self.VM, open(path, 'bw'))
        else:
            raise FileExistsError("File already exists.")
        return 'Save state saved.'

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
        keys = self.VM.keys
        if self.record and keys != self.inputHistory[-1][0]:
            self.inputHistory.append((keys, self.VM.clock))
        if not self.record and not self.done:
            # Use the previous input until the next stored change is encountered
            if self.VM.clock < self.inputHistory[self.historyPos + 1][1]:
                self.input(self.inputHistory[self.historyPos][0])
            else:
                self.historyPos += 1
                self.doneIf(self.historyPos + 1 == len(self.inputHistory))
                self.input(self.inputHistory[self.historyPos][0])
        core.step(self.VM)
        self.aiKeys   = 0
        self.userKeys = 0

    def reset(self):
        '''
        Complete reset to original state. Reloads ROM.
        '''
        logger.info('Resetting vm `{}`'.format(self))
        self.VM = core.initVM(self.__freq // 60)
        if self.ROM:
            self.loadROM(self.ROM, reset=False)
        if self.window:
            self.window.gameModule.clearUpdate()
        return 'Reset.'

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
            if self.done:
                break
            if not self.paused:
                self.input(action)
                self.step()
            if self.window:
                self.input(action)
                self.window.update(self)
                self.window.render(force=self.paused)
                self.window.sound(self.VM.ST > 0)
                self.pyclock.tick(self.__pausedFreq if self.paused else self.__freq)

    def doneIf(self, done):
        '''
        Sets the VM to done if `done` is true. Signals VMs collection if 
        applicable.

        @param done  bool  if done
        '''
        if not self.done and done:
            logger.info('VM is done `{}`'.format(self))
            self.done = True
            if self.__VMs:
                self.__VMs.signalDone(self)
