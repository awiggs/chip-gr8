import logging
import ctypes
import glob
import os

from chipgr8.autogen_Chip8VMStruct import Chip8VMStruct
from chipgr8.fallbackChip8         import FallbackChip8

logger = logging.getLogger(__name__)

USE_PYTHON_FALLBACK = False

def helloSharedLibrary():
    assert lib.helloSharedLibrary() == 0xAFBFCF
    logger.info('DLL loaded succesfully')

def initVM(freq):
    '''
    Allocates and returns a pointer to a VM.
    '''
    if USE_PYTHON_FALLBACK:
        vm = FallbackChip8(freq)
    else:
        vm = Chip8VMStruct()
        lib.initVM(vm, freq)
    logger.debug('Initializing VM {}'.format(vm))
    return vm

def step(vm):
    '''
    Performs a single step on the eprovided VM.
    '''
    if USE_PYTHON_FALLBACK:
        vm.step()
    else:
        lib.step(vm)

def loadROM(vm, filePath):
    '''
    Loads a ROM from filePath into the VM.
    '''
    if USE_PYTHON_FALLBACK:
        return vm.loadROM(filePath)
    else:
        return lib.loadROM(vm, filePath)

def sendInput(vm, keymask):
    '''
    Sends the current input to the VM.
    '''
    if USE_PYTHON_FALLBACK:
        vm.input(keymask)
    else:
        lib.input(vm, keymask)

def repair(vm):
    '''
    Repairs fallback VM after pickling
    '''
    if USE_PYTHON_FALLBACK:
        vm._defineAliases()

dist = glob.glob(os.path.realpath(os.path.join(__file__, '../libchip-gr8.*[!py]')))
DLL_DIST_PATH    = dist[0] if dist else '<No dist path found!>'
DLL_DEBUG_PATH   = os.path.realpath(os.path.join(__file__, '../../target/debug/libchip-gr8'))
DLL_RELEASE_PATH = os.path.realpath(os.path.join(__file__, '../../target/release/libchip-gr8'))

lib = None
for path in [
    DLL_DIST_PATH,
    DLL_DEBUG_PATH,
    DLL_DEBUG_PATH + '.dll',
    DLL_DEBUG_PATH + '.exe',
    DLL_DEBUG_PATH + '.so',
    DLL_RELEASE_PATH,
    DLL_RELEASE_PATH + '.dll',
    DLL_RELEASE_PATH + '.exe',
    DLL_RELEASE_PATH + '.so',
]:
    try:
        lib = ctypes.CDLL(path)
    except Exception as error:
        continue
        
    lib.initVM.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_uint8]
    lib.initVM.restype = None

    lib.step.argtypes = [ctypes.POINTER(Chip8VMStruct)]
    lib.step.restype = None

    lib.loadROM.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_char_p]
    lib.loadROM.restype = ctypes.c_int

    lib.input.argtypes = [ctypes.POINTER(Chip8VMStruct), ctypes.c_ushort]
    lib.input.restype = None
    
    break
else:
    logger.warning('Could not find DLL, using python fallback')
    USE_PYTHON_FALLBACK = True