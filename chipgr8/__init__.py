# Add imports that should be available at the top level of the API
from .chipgr8      import init
from .disassembler import disassemble, hexdump
from .assembler    import assemble
from .util         import findROM, readableInputHistory
from .query        import Query
from .observer     import Observer

themes = {
    'light'    : ('000000', 'FFFFFF'),
    'dark'     : ('FFFFFF', '000000'),
    'sunrise'  : ('ff6464', '780a3c'),
    'hacker'   : ('20C20E', '000000'),
    'redalert' : ('FF0000', '000000'),
    'snake'    : ('00CA83', 'FFFFFF'),
}

VERSION     = '0.0.1'
DESCRIPTION = "Chip-Gr8: The AI focused Chip 8 Emulator"