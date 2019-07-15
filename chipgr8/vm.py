import os
import pygame
import pickle as pkl
import numpy  as np
import json
import sys

import chipgr8.io           as io
import chipgr8.core         as core
import chipgr8.shaders      as shaders
import chipgr8.disassembler as disassembler

from chipgr8.util import write, findROM
from lazyarray    import larray
from collections  import namedtuple

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

    record = True
    '''Flag for recording input history'''

    sampleRate = 1
    '''For AI agents, how many steps are taken per act'''

    stepCounter = 0
    '''How many steps were taken since the last sample'''

    aiKeys = 0
    '''Input last pressed by the AI agent'''

    aiInputMask = 0
    '''Input mask to combine user and AI input'''

    smooth = False
    '''Flag for smooth rendering'''
    
    paused = False
    '''Flag for pausing'''

    window = None
    '''Window instance'''

    userKeys = 0
    '''Current input keys sample'''

    done = False
    '''Indicates whether the VM is in a done state'''

    keyBindings = None

    defaultKeyBindings = {
        "k0" : 120,
        "k1" : 49,
        "k2" : 50,
        "k3" : 51,
        "k4" : 113,
        "k5" : 119,
        "k6" : 101,
        "k7" : 97,
        "k8" : 115,
        "k9" : 100,
        "ka": 122,
        "kb": 99,
        "kc": 52,
        "kd": 114,
        "ke": 102,
        "kf": 118,
        "debugPause": 286,
        "debugStep": 287,
        "debugHome": 278,
        "debugEnd": 279,
        "debugPageUp": 280,
        "debugPageDown": 281
    }

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
        # TODO adjust for Super Chip-48
        width, height = 64, 32

        self.record       = inputHistory is None
        self.inputHistory = inputHistory or []
        self.aiInputMask  = aiInputMask

        self.__freq = (frequency // 60) * 60
        self.smooth = smooth
        self.paused = startPaused
        self.VM     = core.initVM(frequency // 60)
        self.loadROM(ROM)
        self.loadKeyBindings()

        assert inputHistory is None or len(inputHistory) > 1

        self.window = io.ChipGr8Window(width, height) if display else None

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

    def go(self, function=None):
        '''
        Runs displayable VM core loop.

        @params function            The AI agent function
        '''
        assert self.window, 'Cannot start a VM with no window!'
        assert self.ROM,    'Cannot start a VM with no ROM!'

        clk = pygame.time.Clock()
        
        self.window.disModule.initText(self.ROM.encode())
        self.window.clear()
        self.render(forceDissassemblyRender=True)

        historyIdx = 1

        while (self.eventProcessor()):
            if self.paused:
                clk.tick(self.__pausedFreq)
            else:
                if self.record:
                    # Add masked user input to combined input
                    combinedInput = self.userKeys if self.aiInputMask is None else self.userKeys & ~self.aiInputMask
                    if function and self.stepCounter == 0:
                        function(self)
                    combinedInput |= self.aiKeys if self.aiInputMask is None else self.aiKeys & self.aiInputMask
                    self.input(combinedInput, forceSend=True)
                    # Update AI step counter
                    self.stepCounter = (self.stepCounter + 1) % self.sampleRate
                else:
                    # Use the previous input until the next stored change is encountered
                    if self.VM.clock < self.inputHistory[historyIdx][1]:
                        self.input(self.inputHistory[historyIdx-1][0], forceSend=True)
                    else:
                        self.input(self.inputHistory[historyIdx][0], forceSend=True)
                        historyIdx += 1
                        if historyIdx == len(self.inputHistory):
                            break

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

    def input(self, keys, forceSend=False):
        '''
        Set the current VM IO state.

        @params keys    int     
                A raw set of bytes representing the io memory
        '''

        if self.window is None or forceSend:
            if self.record:
                # if keys is the same as the last thing in the input history, don't store it
                if (not self.inputHistory) or (self.inputHistory and (keys != self.inputHistory[-1][0])):
                    self.inputHistory.append((keys, self.VM.clock))
            core.sendInput(self.VM, keys)
        else:
            self.aiKeys = keys

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
                
            self.window.disModule.render(override=forceDissassemblyRender, highlight=pcHighlight)
            self.window.consoleModule.render()
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
        ROM_temp = self.ROM
        self.VM = core.initVM(self.__freq // 60)
        self.ROM = ROM_temp

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
                    if event.key == self.keyBindings["debugPause"]:
                        self.togglePause()
                    elif event.key == self.keyBindings["debugStep"] and self.paused:
                        self.step()
                        self.highlightDisassembly()
                    elif event.key == self.keyBindings["debugPageUp"]:
                        self.scrollDisassemblyUp(numLines=4)
                    elif event.key == self.keyBindings["debugPageDown"]:
                        self.scrollDisassemblyDown(numLines=4)
                    elif event.key == self.keyBindings["debugHome"]:
                        self.scrollDisassemblyUp()
                    elif event.key == self.keyBindings["debugEnd"]:
                        self.scrollDisassemblyDown()

                if self.paused:
                    self.window.consoleModule.update(event)
                else:
                    self.keyProcessor(event)

        return True
        
    def keyProcessor(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keyBindings["k0"]:
                self.userKeys |= 1
            elif event.key == self.keyBindings["k1"]:
                self.userKeys |= 1 << 1
            elif event.key == self.keyBindings["k2"]:
                self.userKeys |= 1 << 2
            elif event.key == self.keyBindings["k3"]:
                self.userKeys |= 1 << 3
            elif event.key == self.keyBindings["k4"]:
                self.userKeys |= 1 << 4
            elif event.key == self.keyBindings["k5"]:
                self.userKeys |= 1 << 5
            elif event.key == self.keyBindings["k6"]:
                self.userKeys |= 1 << 6
            elif event.key == self.keyBindings["k7"]:
                self.userKeys |= 1 << 7
            elif event.key == self.keyBindings["k8"]:
                self.userKeys |= 1 << 8
            elif event.key == self.keyBindings["k9"]:
                self.userKeys |= 1 << 9
            elif event.key == self.keyBindings["ka"]:
                self.userKeys |= 1 << 10
            elif event.key == self.keyBindings["kb"]:
                self.userKeys |= 1 << 11
            elif event.key == self.keyBindings["kc"]:
                self.userKeys |= 1 << 12
            elif event.key == self.keyBindings["kd"]:
                self.userKeys |= 1 << 13
            elif event.key == self.keyBindings["ke"]:
                self.userKeys |= 1 << 14
            elif event.key == self.keyBindings["kf"]:
                self.userKeys |= 1 << 15
            
        if event.type == pygame.KEYUP:
            if event.key == self.keyBindings["k0"]:
                self.userKeys &= ~(1)
            elif event.key == self.keyBindings["k1"]:
                self.userKeys &= ~(1 << 1)
            elif event.key == self.keyBindings["k2"]:
                self.userKeys &= ~(1 << 2)
            elif event.key == self.keyBindings["k3"]:
                self.userKeys &= ~(1 << 3)
            elif event.key == self.keyBindings["k4"]:
                self.userKeys &= ~(1 << 4)
            elif event.key == self.keyBindings["k5"]:
                self.userKeys &= ~(1 << 5)
            elif event.key == self.keyBindings["k6"]:
                self.userKeys &= ~(1 << 6)
            elif event.key == self.keyBindings["k7"]:
                self.userKeys &= ~(1 << 7)
            elif event.key == self.keyBindings["k8"]:
                self.userKeys &= ~(1 << 8)
            elif event.key == self.keyBindings["k9"]:
                self.userKeys &= ~(1 << 9)
            elif event.key == self.keyBindings["ka"]:
                self.userKeys &= ~(1 << 10)
            elif event.key == self.keyBindings["kb"]:
                self.userKeys &= ~(1 << 11)
            elif event.key == self.keyBindings["kc"]:
                self.userKeys &= ~(1 << 12)
            elif event.key == self.keyBindings["kd"]:
                self.userKeys &= ~(1 << 13)
            elif event.key == self.keyBindings["ke"]:
                self.userKeys &= ~(1 << 14)
            elif event.key == self.keyBindings["kf"]:
                self.userKeys &= ~(1 << 15)

    # UI Actions

    def togglePause(self):
        self.paused = not self.paused
        self.highlightDisassembly()

    def scrollDisassemblyUp(self, numLines=None):
        if self.window:
            if numLines == None:
                self.window.disModule.scrollDissassemblyToLine(0)
            else:
                self.window.disModule.offsetScrollDisassembly(-1 * numLines)

    def scrollDisassemblyDown(self, numLines=None):
        if self.window:
            if numLines == None:
                self.window.disModule.scrollDissassemblyToLine(self.window.disModule.getLastDisassemblyLine(), centre=False)
            else:
                self.window.disModule.offsetScrollDisassembly(numLines)

    def highlightDisassembly(self):
        if self.window:
            self.window.disModule.setWarningStatus(core.getProgramCounter(self.VM) % 2 == 1)
            line = (core.getProgramCounter(self.VM) - 512) // 2 + 1 # Offset interpret space and add 1 because 1-indexing
            self.window.disModule.setCurrDisassemblyLine(line)
            self.window.disModule.scrollDissassemblyToCurrLine()

    def loadKeyBindings(self):
        try: 
            f = open("KeyConfig.json")
            bindings = json.load(f)
            self.keyBindings = bindings
        except:
            print("KeyBindings configuration file not found.")
        self.sanityCheckBindings()

    def sanityCheckBindings(self):
        validKeyConfig = True
        bindingsUsed = []
        validKeys = list(self.defaultKeyBindings.keys())

        if self.keyBindings is None:
            validKeyConfig = False
        else:
            for key in self.keyBindings:
                if self.keyBindings[key] not in bindingsUsed and isinstance(self.keyBindings[key], int):
                    bindingsUsed.append(self.keyBindings[key])
                else:
                    validKeyConfig = False
                    break

                try:
                    validKeys.remove(key)
                except:
                    validKeyConfig = False
                    break

            if(not len(validKeys) == 0):
                validKeyConfig = False

        if (not validKeyConfig):
            response = input("KeyConfig.json file is corrupted.\nWould you like to restore default key bindings? (Y/n)")
            if response == "Y" or response == "y":
                self.updateKeyBindings(self.defaultKeyBindings)
            else:
                print("Program cannot proceed with corrupted bindings, shutting down...")
                sys.exit()

    def updateKeyBindings(self, bindings):
        f = open("KeyConfig.json", "w")
        json.dump(bindings, f, indent=4)

    def setKeyBinding(self, newBindDict):
        validKeys = list(self.defaultKeyBindings.keys())
        invallidValues = list(self.keyBindings.values())
        for key in newBindDict:
            if key in self.keyBindings:
                invallidValues.remove(self.keyBindings[key])    

        for key in newBindDict:
            if key not in validKeys:
                raise Exception("Invallid Binding. Key: " + key + " is not a valid key.\nUse 'print(vm.defaultKeyBindings.keys())' to see all valid keys.")
            elif not isinstance(newBindDict[key], int):
                raise Exception("Invallid Binding. Binding value: " + str(newBindDict[key]) + " is not an integer. Values must be integers")
            elif newBindDict[key] in invallidValues:
                raise Exception("Invallid Binding. Binding value: " + str(newBindDict[key]) + " is already in use. Try 'print(list(vm.keyBindings.values())) to see a list of all currently used bindings.")
            else:
                self.keyBindings[key] = newBindDict[key]
                self.updateKeyBindings(self.keyBindings)
