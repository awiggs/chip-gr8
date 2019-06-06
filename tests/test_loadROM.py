#!/usr/bin/python3.7
from chipgr8.vm import Chip8VM as vm

c = vm()

c.loadROM("test.c8")
c.unloadROM()
