import ctypes
import os

from chipgr8.autogen_Chip8VMStruct import Chip8VMStruct

def helloSharedLibrary():
    assert lib.helloSharedLibrary() == 0xAFBFCF
    print('DLL loaded succesfully')

def initVM(freq):
    '''
    Allocates and returns a pointer to a VM.
    '''
    vm = Chip8VMStruct()
    lib.initVM(vm, freq)
    return vm

def freeVM(vm):
    '''
    Deallocates the provided VM.
    '''
    lib.freeVM(vm)

def step(vm):
    '''
    Performs a single step on the eprovided VM.
    '''
    return lib.step(vm)

def loadROM(vm, filePath):
    '''
    Loads a ROM from filePath into the VM.
    '''
    return lib.loadROM(vm, filePath)

def unloadROM(vm):
    '''
    Unloades a ROM, if one was loaded previously, from a VM.
    '''
    return lib.unloadROM(vm)

def sendInput(vm, keymask):
    '''
    Sends the current input to the VM.
    '''
    return lib.input(vm, keymask)

DLL_DEBUG_PATH   = os.path.realpath(os.path.join(__file__, '../../target/debug/libchip-gr8'))
DLL_RELEASE_PATH = os.path.realpath(os.path.join(__file__, '../../target/release/libchip-gr8'))

lib = None
for path in [
    DLL_DEBUG_PATH,
    DLL_DEBUG_PATH + '.dll',
    DLL_DEBUG_PATH + '.exe',
    DLL_DEBUG_PATH + '.so',
    DLL_RELEASE_PATH,
    DLL_RELEASE_PATH + '.dll',
    DLL_RELEASE_PATH + '.exe',
    DLL_RELEASE_PATH + '.so',
]:
    if os.path.isfile(path):
        lib = ctypes.CDLL(path)
        
        lib.initVM.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_uint8]
        lib.initVM.restype = None

        lib.freeVM.argtypes = [ctypes.POINTER(Chip8VMStruct)]
        lib.freeVM.restype = None

        lib.step.argtypes = [ctypes.POINTER(Chip8VMStruct)]
        lib.step.restype = None

        lib.loadROM.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_char_p]
        lib.loadROM.restype = ctypes.c_int

        # TODO unloadROM ctypes specifications
        # lib.unloadROM.argtypes = []
        # lib.unloadROM.restype = 

        lib.input.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_ushort]
        lib.input.restype = None

        break

else:
    raise Exception('DLL has not been built!\nRun `mekpie build`!')
