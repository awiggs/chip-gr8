import ctypes
import os

DLL_DEBUG_PATH   = os.path.realpath(os.path.join(__file__, '../../target/debug/chip-gr8'))
DLL_RELEASE_PATH = os.path.realpath(os.path.join(__file__, '../../target/release/chip-gr8'))

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
        dll = ctypes.CDLL(path)
        break
else:
    raise Exception('DLL has not been built!\nRun `mekpie build`!')

def init():
    raise Exception('Implement Me!')

def helloWorld():
    dll.helloWorld()