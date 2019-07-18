import chipgr8
import os

from chipgr8.util import read

ROMS_PATH = os.path.realpath(os.path.join(__file__, '../data/roms'))

def test_assembler_disassembler():
    for rom in os.listdir(ROMS_PATH):
        if rom.endswith('ch8'):
            rom_path = os.path.join(ROMS_PATH, rom)
            source = chipgr8.disassemble(inPath=rom_path)
            binary = chipgr8.assemble(source)
            assert chipgr8.hexdump(binary) == chipgr8.hexdump(inPath=rom_path)