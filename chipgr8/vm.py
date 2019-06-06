import os
import pickle as pkl
import chipgr8.core as core
import chipgr8.io

class Chip8VM(object):
    '''
    Wraps the Chip8VMStruct object produced by core.initVM and provides a 
    pythonic interface to the VM state.
    '''
    vm = None
    window = None

    def __init__(
        self,
        display   = False,
        timing    = False,
    ):
        '''
        Initializes a new Chip8VM object, calling core.initVM to allocate a new
        C struct.
        '''
        self.vm = core.initVM()

        if display:
            self.window = io.ChipGr8Window() 

    def __del__(self):
        '''
        Destructor needs to call core.freeVM with the struct allocated in the
        constructor.
        '''
        if not self.vm == None:
            core.freeVM(self.vm)


    # ROM Methhods

    def loadROM(self, nameOrPath):
        '''
        Load a ROM from the given path, or check if it is the name of a ROM in
        `data/roms`. Throws an error if no ROM could be found. Internally calls
        core.loadROM.

        @params nameOrPath The name or path of the ROM to load
        '''
        if self.vm == None:
            raise RuntimeError("VM not loaded.")

        if not os.path.isfile(nameOrPath):
            raise FileNotFoundError("The specified file does not exist.")

        core.loadROM(self.vm, nameOrPath)

    def unloadROM(self):
        '''
        Unloads a ROM if one is loaded. Internally calls core.unloadROM.
        '''
        core.unloadROM()
    
    # State Methods

    def loadState(self, path=None, tag=None):
        '''
        Load state from a file or from a tag. Tagged states are stored in 
        `data/tags`. If no file can be provided throws an error.

        @params path If provided, the path to load the state from
                tag  If provided, the tag of the state
        '''
        #TODO: What are tags

        if not ls.path.isfile(path):
            raise FileNotFoundError("Save state file not found.")
        
        self.vm = pkl.load(open(path, 'rb'))

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
            pkl.dump(self.vm, open(path, 'bw'))
        else:
            raise FileExistsError("File already exists.")


    # IO Methods

    def io(
        self, 
        raw     = None, 
        handler = None, 
        # Individual keys
        k1=None, k2=None, k3=None, kC=None,
        k4=None, k5=None, k6=None, kD=None,
        k7=None, k8=None, k9=None, kE=None,
        kA=None, k0=None, kB=None, kF=None,
    ):
        '''
        Set the current VM IO state.

        @params raw     A raw set of bytes representing the io memory
                handler A function that accepts VM state and returns IO
                kX      Explicit parameters for each key
        '''
        if not raw == None:
            core.send_input(raw)
            return
        
        if not handler == None:
            raise NotImplementedError("Handler arguement has not been implemented yet.")

        keymask = bin(0)

        if not k0 == None: keymask += bin(k0)
        if not k1 == None: keymask += bin(k1) << 1
        if not k2 == None: keymask += bin(k2) << 2
        if not k3 == None: keymask += bin(k3) << 3
        if not k4 == None: keymask += bin(k4) << 4
        if not k5 == None: keymask += bin(k5) << 5
        if not k6 == None: keymask += bin(k6) << 6
        if not k7 == None: keymask += bin(k7) << 7
        if not k8 == None: keymask += bin(k8) << 8
        if not k9 == None: keymask += bin(k9) << 9
        if not kA == None: keymask += bin(kA) << 10
        if not kB == None: keymask += bin(kB) << 11
        if not kC == None: keymask += bin(kC) << 12
        if not kD == None: keymask += bin(kD) << 13
        if not kE == None: keymask += bin(kE) << 14
        if not kF == None: keymask += bin(kF) << 15

        core.send_input(keymask)


    def render(self):
        '''
        Force a render to the window (if it is open).
        '''
        if not self.window == None:
            self.window.render(self.VRAM(), True) 
    
    # State Methods

    def step(self):
        '''
        Simulate a single VM clock cycle. Internally calls core.step.
        '''
        core.step(vm)

    def steps(self, n):
        '''
        Simulate a number of clock cycles in a row. Internally calls core.step.
        '''
        while n > 0:
            core.step(vm)
            n -= 1

    # Data Fields

    def VRAM(self):
        '''
        The VM VRAM in a bitmap format (32x64) where the first bitmap[row] 
        indexes through each row and index[row][col] indexes through each pixel.
        Each pixel is either 0 or 1 (black or white).

        @returns the bitmap
        '''
        ptrVRAM = core.getVRAM(vm)
        print(ptrVRAM)
        pass #TODO
