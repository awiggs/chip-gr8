import chipgr8.core as core

class Chip8VM(object):
    '''
    Wraps the Chip8VMStruct object produced by core.initVM and provides a 
    pythonic interface to the VM state.
    '''

    def __init__(
        self,
        display   = None,
        timing    = None,
    ):
        '''
        Initializes a new Chip8VM object, calling core.initVM to allocate a new
        C struct.
        '''
        # core.initVM()
        pass #TODO

    def __del__(self):
        '''
        Destructor needs to call core.freeVM with the struct allocated in the
        constructor.
        '''
        # core.freeVM()
        pass #TODO


    # ROM Methhods

    def loadROM(nameOrPath):
        '''
        Load a ROM from the given path, or check if it is the name of a ROM in
        `data/roms`. Throws an error if no ROM could be found. Internally calls
        core.loadROM.

        @params nameOrPath The name or path of the ROM to load
        '''
        pass #TODO

    def unloadROM():
        '''
        Unloads a ROM if one is loaded. Internally calls core.unloadROM.
        '''
        pass #TODO
    
    # State Methods

    def loadState(path=None, tag=None):
        '''
        Load state from a file or from a tag. Tagged states are stored in 
        `data/tags`. If no file can be provided throws an error.

        @params path If provided, the path to load the state from
                tag  If provided, the tag of the state
        '''
        pass #TODO

    def saveState(path=None, tag=None, force=False):
        '''
        Save state to a file or to a tag (ie. `data/tags/<tag>`).
        
        @params path  If provided, the path to save the state to
                tag   If provided, the tag to save the state to
                force If true, overwrite already existing files, otherwise
                      throw an error
        '''
        pass #TODO


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
        pass #TODO

    def render():
        '''
        Force a render to the window (if it is open).
        '''
        pass #TODO

    
    # State Methods

    def step(self):
        '''
        Simulate a single VM clock cycle. Internally calls core.step.
        '''
        pass #TODO

    def steps(self, n):
        '''
        Simulate a number of clock cycles in a row. Internally calls core.step.
        '''
        pass #TODO

    # Data Fields

    def VRAM(self):
        '''
        The VM VRAM in a bitmap format (32x64) where the first bitmap[row] 
        indexes through each row and index[row][col] indexes through each pixel.
        Each pixel is either 0 or 1 (black or white).

        @returns the bitmap
        '''
        pass #TODO