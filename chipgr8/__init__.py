# Add imports that should be available at the top level of the API
from .chipgr8      import init
from .disassembler import disassemble, hexdump
from .assembler    import assemble
from .util         import findROM
from .query        import Query

VERSION     = '0.0.1'
DESCRIPTION = "ChipGr8: The AI focused Chip 8 Emulator"