import ctypes
import os

DLL_DEBUG_PATH   = os.path.realpath(os.path.join(__file__, '../../target/debug/libchip-gr8'))
DLL_RELEASE_PATH = os.path.realpath(os.path.join(__file__, '../../target/release/libchip-gr8'))

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
        break
else:
    raise Exception('DLL has not been built!\nRun `mekpie build`!')

#TODO Provide ctypes specifications for all of the following functions

def helloSharedLibrary():
    assert lib.helloSharedLibrary() == 0xAFBFCF
    print('DLL loaded succesfully')

def initVM():
    '''
    Allocates and returns a pointer to a VM.
    '''
    return lib.initVM()

def freeVM(vm):
    '''
    Deallocates the provided VM.
    '''
    return lib.freeVM(vm)

def step(vm):
    '''
    Performs a single step on the eprovided VM.
    '''
    return lib.step(vm)

def loadROM(vm, filePath):
    '''
    Loads a ROM from filePath into the VM.
    '''
    return lib.loadVM(vm, filePath)

def unloadROM(vm):
    '''
    Unloades a ROM, if one was loaded previously, from a VM.
    '''
    return lib.unloadROM(vm)

class Chip8VMStruct(ctypes.Structure):
    '''
    A close wrapping of the C struct Chip8VM_t using ctypes. This wrapper will
    NOT be used directly by the other parts of the application, instead 
    instances of this class will be wrapped in a Chip8VM vm instance (found in
    `chipgr8/vm.py`).

    This class provides access to read/write all of the fields found in
    the struct Chip8VM_t (defined in `includes/chip8.h`).
    '''
    pass #TODO