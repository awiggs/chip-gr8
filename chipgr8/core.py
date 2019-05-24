import ctypes
import os

DLL_DEBUG_PATH = os.path.realpath(os.path.join(__file__, '../../target/debug/chip-gr8'))

DLL_RELEASE_PATH = os.path.realpath(os.path.join(__file__, '../../target/release/chip-gr8'))

print (DLL_DEBUG_PATH)

if os.path.exists(DLL_DEBUG_PATH):
    dll = ctypes.CDLL(DLL_DEBUG_PATH)
elif os.path.exists(DLL_RELEASE_PATH):
    dll = ctypes.CDLL(DLL_RELEASE_PATH)
else:
    raise Exception('DLL has not been built!\nRun `mekpie build`!')

def init():
    raise Exception('Implement Me!')

def helloWorld():
    dll.helloWorld()