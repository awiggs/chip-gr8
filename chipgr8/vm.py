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

SHIFT_QUIRK = 0x01
LOAD_QUIRK  = 0x02
DRAW_QUIRK  = 0x04

quirks = {
    "Animal Race.ch8": SHIFT_QUIRK | LOAD_QUIRK,
    "Astro Dodge.ch8": DRAW_QUIRK,
    "Blinky.ch8": LOAD_QUIRK,
    "Space Invaders.ch8": LOAD_QUIRK,
}

class Chip8VM(object):
    '''
    Represents a CHIP-8 virtual machine. Provides interface and controls for 
    display and input. Rather than initializing directly, an instance of this 
    class or its sister class Chip8VMs should always be instantiated using init.
    '''

    __pausedFreq = 30
    '''
    The VM paused frequency
    '''

    __VMs = None
    '''
    Containing VM collection
    '''

    __ctx = None
    '''
    Graphics content cache. We need to keep this variable private as it must be 
    cleared prior to pickling the vm instance.
    '''

    __freq = 600
    '''
    The VM runnning frequency
    '''

    __userKeys = 0
    '''
    Current input keys sample
    '''

    __aiKeys = 0
    '''
    Input last pressed by the AI agent
    '''

    __historyPos = 0
    '''
    Index of history for playback
    '''

    __done = False
    '''
    Indicates whether the VM is in a done state
    '''

    __breakpoints = []
    '''
    Breakpoints
    '''

    _window = None
    '''
    Window instance
    '''

    aiInputMask = 0
    '''
    A number that controls what keys are usable by AI agents calling act and 
    what keys are usable by a user on their keyboard. For example, An 
    aiInputMask of 0x0000 will prevent an AI agent from using any keys, but a 
    user will be able to use all keys.
    '''

    inputHistory = []
    '''
    A list of number pairs that represent changes in key presses. The first 
    value in the pair is the key value, the second is the clock value when input 
    changed to that value.
    '''

    paused = False
    '''
    A control flag set to True if the display is paused.
    '''

    pyclock = None
    '''
    The pygame clock used to keep track of time between steps when using the 
    CHIP-GR8 display.
    '''

    record = True
    '''
    A control flag set to True if inputHistory is being recorded.
    '''

    ROM = None
    '''
    The path to the currently loaded game ROM.
    '''

    sampleRate = 1
    '''
    The number of steps that are performed when an AI calls act.
    '''

    smooth = False
    '''
    A control flag for the experimental smooth rendering mode. This mode is 
    slow on most machines.
    '''

    VM = None
    '''
    A direct reference to the CHIP-8 c-struct. This provides direct memory 
    access (eg. VM.RAM[0x200]) as well as register reference (eg. VM.PC). Use 
    these fields with caution as inappropriate usage can result in a 
    segmentation fault. Direct references to VM should not be maintained 
    (no aliasing).
    s'''

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
        autoScroll,
        speed,
    ):
        '''
        Initializes a new Chip8VM object. Responsible for allocating a new VM
        struct, game _window, etc. If called with display equal to true will
        begin the game loop.

        @params ROM               str               name or path to the ROM to load
                frequency         int               frequency to run the VM at
                loadState         str               path or tag to a save state
                inputHistory      List[(int, int)]  a list of predifined IO events
                sampleRate        int               how many steps act moves forward
                display           bool              if true creates a game _window
                smooth            bool              if true uses smooth rendering
                startPaused       bool              if true starts the vm paused
                shader            Shader            display shader to use
                aiInputMask       int               A mask for combining user and AI inputs. If
                                                    any 16-bit integer, inputs made by the AI for
                                                    keys masked with 0 will be ignored. Inputs made
                                                    by a user for keys masked with 1 will also be ignored.
                foreground        (int, int, int)   hex color code or color tuple
                background        (int, int, int)   hex color code or color tuple
                autoScroll bool              if false, disModule will not 
                                                    scroll to highlighted code
        '''
        assert inputHistory is None or len(inputHistory) > 1, 'Input history mut have recorded at least two key presses!'

        self.sampleRate   = sampleRate
        self.speed        = int(speed)
        self.record       = inputHistory is None
        self.inputHistory = inputHistory or [(0, 0)]
        self.aiInputMask  = aiInputMask
        self.smooth       = smooth
        self.paused       = startPaused
        self.VM           = core.initVM(frequency // 60)
        self.autoScroll   = autoScroll
        self.__historyPos = 0
        self.__freq       = (frequency // 60) * 60
        if ROM:
            self.loadROM(ROM, reset=False)
        self._window = Window(
            64, 32, 
            foreground = foreground, 
            background = background
        ) if display else None
        self.pyclock = pygame.time.Clock() if display else None

    def _linkVMs(self, VMs):
        '''
        Links VM with a VM collection.

        @param VMs  Chip8VMs     the collection to link to
        '''
        self.__VMs = VMs

    def _clearCtx(self):
        self.__ctx = None

    def addBreakpoint(self, addr):
        '''
        Add a breakpoint at addr. When the VM steps to this address (when PC is
        equal to addr) the CHIP-GR8 display will automatically pause.
        '''
        self.__breakpoints.append(addr)
        if self._window:
            self._window.render(force=True, breakpoints=self.__breakpoints)
        return 'Breakpoint added. (0x{:x})'.format(addr)

    def removeBreakpoint(self, addr):
        '''
        Remove a breakpoint at addr.
        '''
        self.__breakpoints.remove(addr)
        if self._window:
            self._window.render(force=True, breakpoints=self.__breakpoints)
        return 'Breakpoint removed. (0x{:x})'.format(addr)

    def toggleBreakpoint(self, addr):
        '''
        Toggles a breakpoint at addr.
        '''
        if addr in self.__breakpoints:
            return self.removeBreakpoint(addr)
        else:
            return self.addBreakpoint(addr)

    def clearBreakpoints(self):
        '''
        Clear all current breakpoints.
        '''
        self.__breakpoints.clear()
        if self._window:
            self._window.render(force=True, breakpoints=self.__breakpoints)
        return 'Breakpoints cleared.'

    def ctx(self):
        '''
        Returns an instance of the CHIP-8’s VRAM in a numpy compliant format 
        (lazyarray). Pixel values can be addressed directly. (eg. a pixel at 
        position (16, 8) can be retrieved with ctx()[16, 8]). This method is 
        safe to call repeatedly.
        '''
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

    def act(self, action, repeat=1):
        '''
        Allows an AI agent to perform action (action is an input key value) and 
        steps the CHIP-8 emulator forward sampleRate clock cycles.
        '''
        for _ in range(repeat):
            for _ in range(self.sampleRate):
                if self.done():
                    break
                if not self.paused:
                    self.input(action)
                    self.step()
                if self._window:
                    self.input(action)
                    self._window.update(self)
                    if self.paused or not self.VM.clock % self.speed:
                        self._window.render(force=self.paused, breakpoints=self.__breakpoints)
                    self._window.sound(self.VM.ST > 0)
                    self.pyclock.tick(self.__pausedFreq if self.paused else self.__freq * self.speed)

    def actUntil(self, action, predicate):
        '''
        Performs act(action) in a loop until the provided predicate returns 
        true. The predicate is called with the vm instance. 
        '''
        while not predicate(self) and not self.done():
            self.act(action)

    def done(self):
        '''
        Returns True if the VM is done and has NOT been reset.
        '''
        return self.__done

    def doneIf(self, done):
        '''
        Signals to the VM that it is done.
        '''
        if not self.__done and done:
            logger.info('VM is done `{}`'.format(self))
            self.__done = True
            if self.__VMs:
                self.__VMs._signalDone(self)

    def go(self):
        '''
        Starts the VM in an until done() loop, calling act(0) repeatedly. This 
        is ideal for user interaction without an AI agent.	
        '''
        assert self._window, 'Cannot use `go` without a _window'
        logger.info('VM starting in user mode (go) `{}`'.format(self))
        try:
            while not self.done():
                self.act(0)
        except KeyboardInterrupt:
            print('Goodbye!')

    def input(self, keys, user=False):
        '''
        Send an input key value to the CHIP-8 emulator. Input keys are masked by
        aiInputMask.	
        '''
        if user:
            self.__userKeys = keys
        else:
            self.__aiKeys = keys
        core.sendInput(
            self.VM, 
            (self.__aiKeys   &  self.aiInputMask) | 
            (self.__userKeys & ~self.aiInputMask),
        )

    def loadROM(self, nameOrPath, reset=True):
        '''
        Loads a ROM from the provided path or searches for the name in the set 
        of provided ROM files. If reset is True the VM will be reset prior to 
        loading the ROM.
        '''
        logger.info('Loading rom `{}` into `{}`'.format(nameOrPath, self))
        if reset:
            self.reset()
        self.ROM       = findROM(nameOrPath)
        self.VM.quirks = quirks.get(os.path.basename(self.ROM), 0x00)
        if not self.ROM:
            raise FileNotFoundError("ROM `{}` does not exist.".format(self.ROM))
        if not core.loadROM(self.VM, self.ROM.encode()):
            raise RuntimeError("Library failed to load ROM.")
        if self._window:
            self._window.refresh(self)
        return 'Loaded ROM.'
    
    def loadState(self, path=None, tag=None):
        '''
        Load a CHIP-8 emulator state from a path or by associated tag, restoring 
        a previous state of VM.
        '''
        assert path or tag
        logger.info('Loading state from `{}` into `{}`'.format(path or tag, self))
        if tag:
            path = resolveTag(tag)
        if not os.path.isfile(path):
            raise FileNotFoundError("Save state file not found.")
        self.VM = pickle.load(open(path, 'rb'))
        if self._window:
            self._window.refresh(self)
        return 'Save state loaded.'

    def saveState(self, path=None, tag=None, force=False):
        '''
        Save the current CHIP-8 emulator state to a path or tag. If force is 
        True files will be overwritten. 
        '''
        assert path or tag
        logger.info('Saving state to `{}` for `{}`'.format(path or tag, self))
        if tag:
            path = resolveTag(tag)
        if not os.path.exists(path) or force:
            pickle.dump(self.VM, open(path, 'bw'))
        else:
            raise FileExistsError("File already exists.")
        return 'Save state saved.'

    def reset(self):
        '''
        Reset the VM with the current ROM still loaded.
        '''
        logger.info('Resetting vm `{}`'.format(self))
        self.VM = core.initVM(self.__freq // 60)
        if self.ROM:
            self.loadROM(self.ROM, reset=False)
        if self._window:
            self._window.gameModule.clearUpdate()
        return 'Reset.'
    
    def step(self):
        '''
        Step the VM forward 1 clock cycle.
        '''
        keys = self.VM.K
        if self.record and keys != self.inputHistory[-1][0]:
            self.inputHistory.append((keys, self.VM.clock))
        if not self.record and not self.done():
            # Use the previous input until the next stored change is encountered
            if self.VM.clock < self.inputHistory[self.__historyPos + 1][1]:
                self.input(self.inputHistory[self.__historyPos][0])
            else:
                self.__historyPos += 1
                self.doneIf(self.__historyPos + 1 == len(self.inputHistory))
                self.input(self.inputHistory[self.__historyPos][0])
        core.step(self.VM)
        self.__aiKeys   = 0
        self.__userKeys = 0
        if self.VM.PC in self.__breakpoints:
            self.paused = True