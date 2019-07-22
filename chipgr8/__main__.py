import sys
import chipgr8
import logging
import argparse

'''
Parse command line arguments and provide the appropriate options to init. 

ChipGr8: The AI focused Chip 8 Emulator

usage: chipgr8 [-h] [-v] [-vvv] [-r ROM] [-a SOURCE] [-d BINARY] [-o OUT] [-n]
               [-x] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -vvv, --verbose       show more information on the console while running
  -r ROM, --rom ROM     provide a chip 8 ROM to run
  -a SOURCE, --assemble SOURCE
                        run the assembler with input SOURCE
  -d BINARY, --disassemble BINARY
                        run this disassembler with input BINARY
  -o OUT, --out OUT     output file for assembler/disassembler
  -n, --nolabels        do not generate labels in disassembly
  -x, --hexdump         show hex in disassembly
  -s, --smooth          enable smooth rendering mode
'''

parser = argparse.ArgumentParser(
    prog         = 'chipgr8',
    description  = chipgr8.DESCRIPTION,
    #allow_abbrev = False, 
)
parser.add_argument('-V', '--version',
    action  = 'version',
    version = 'chipgr8 ' + chipgr8.VERSION,
)
parser.add_argument('-v', '--verbose',
    action  = 'count',
    default = 0,
    help    = 'show more information on the console while running (-v for some, -vvv for more)', 
)
parser.add_argument('-r', '--rom',
    action = 'store',
    help   = 'provide a chip 8 ROM to run',
)
parser.add_argument('-a', '--assemble',
    action = 'store',
    dest   = 'source',
    help   = 'run the assembler with input SOURCE',
)
parser.add_argument('-d', '--disassemble',
    action = 'store',
    dest   = 'binary',
    help   = 'run this disassembler with input BINARY',
)
parser.add_argument('-o', '--out',
    action = 'store',
    dest   = 'out',
    help   = 'output file for assembler/disassembler',
)
parser.add_argument('-L', '--no-labels',
    action = 'store_true',
    help   = 'do not generate labels in disassembly',
)
parser.add_argument('-x', '--hexdump',
    action = 'store_true',
    help   = 'show hex in disassembly',
)
parser.add_argument('-s', '--smooth',
    action = 'store_true',
    help   = 'enable smooth rendering mode (experimental)',
)
parser.add_argument('-f', '--foreground',
    action = 'store',
    help   = 'display foreground',
)
parser.add_argument('-b', '--background',
    action = 'store',
    help   = 'display background',
)
parser.add_argument('-t', '--theme',
    action  = 'store',
    choices = chipgr8.themes.keys(),
    help    = 'display theme'
)
parser.add_argument('-S', '--no-scroll',
    action  = 'store_false',
    help    = 'reduce flashing in disassembler by not scrolling to the highlighted position')

args      = parser.parse_args()
logLevels = [
    logging.ERROR, 
    logging.WARNING, 
    logging.INFO, 
    logging.DEBUG,
]
logging.basicConfig(
    level=logLevels[min(len(logLevels) - 1, args.verbose)]
)

if args.source:
    result = chipgr8.assemble(inPath=args.source, outPath=args.out)
    if not args.out:
        print(result)
elif args.binary:
    result = chipgr8.disassemble(
        inPath  = chipgr8.findROM(args.binary),
        outPath = args.out, 
        labels  = None if args.nolabels else {},
        hexdump = args.hexdump,
    )
    if not args.out:
        print(result)
else:
    foreground, background = chipgr8.themes.get(
        args.theme, 
        chipgr8.themes['dark']
    )
    chipgr8.init(
        smooth      = args.smooth,
        ROM         = chipgr8.findROM(args.rom) if args.rom else None, 
        startPaused = not args.rom,
        display     = True,
        aiInputMask = 0,
        foreground  = ('#' + args.foreground) if args.foreground else foreground,
        background  = ('#' + args.background) if args.background else background,
        autoScroll  = args.no_scroll,
    ).go()
