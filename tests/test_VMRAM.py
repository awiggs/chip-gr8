from chipgr8.vm import Chip8VM as vm
from chipgr8.io import ChipGr8Window as window 
from tests.util import *

v = vm(display=True)
v.vm.VRAM = getTestBitMap()
