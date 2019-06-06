#!/usr/bin/python3.7
import os, sys
sys.path.append(os.path.expanduser('~/GitHub/chip-gr8'))

import chipgr8.vm as vm

c = vm.Chip8VM(True, False)
bitmap = c.VRAM()

c.render()

