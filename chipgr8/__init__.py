# Hide pygame support message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# Add imports that should be available at the top level of the API
from .chipgr8       import init
from .disassembler  import disassemble, hexdump
from .assembler     import assemble
from .util          import findROM, readableInputHistory, read, findVersion
from .query         import Query
from .observer      import Observer
from .namedList     import NamedList
from .controlModule import ControlModule
from .games         import (
    K_NONE,
    K_0, K_1, K_2, K_3,
    K_4, K_5, K_6, K_7,
    K_8, K_9, K_A, K_B,
    K_C, K_D, K_E, K_F,
)

defaultBindings = ControlModule.defaultBindings
'''
Default key bindings for the CHIP-GR8 display as a python dictionary.
'''

themes = {
    'light'    : ('#000000', '#FFFFFF'),
    'dark'     : ('#FFFFFF', '#000000'),
    'sunrise'  : ('#ff6464', '#780a3c'),
    'hacker'   : ('#20C20E', '#000000'),
    'redalert' : ('#FF0000', '#000000'),
    'snake'    : ('#00CA83', '#FFFFFF'),
}

VERSION     = findVersion()
DESCRIPTION = "Chip-Gr8: The AI focused Chip 8 Emulator"