import chipgr8
import argparse
import sys

'''
Parse command line arguments and provide the appropriate options to init. 

usage: chipgr8 
    -v --version The version number
    -vvv --verbose Print verbose print statements to console during execution
    -h --help    A help message
    -r --rom     The path or name of a rom
    -a --assemble Assemble a text file into a chip 8 rom file
    -d --disassemble Disassemble a chip 8 rom file into a text file
'''


# Parse command line arguments and pass appropriate parameters to init
parser = argparse.ArgumentParser(
    prog         = 'chipgr8',
    description  = chipgr8.DESCRIPTION,
    allow_abbrev = False, 
)
parser.add_argument('-v', '--version',
    action  = 'version',
    version = 'chipgr8 ' + chipgr8.VERSION,
)
parser.add_argument('-vvv', '--verbose',
    action = 'store_true',
    help   = 'show more information on the console while running', 
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
parser.add_argument('-n', '--nolabels',
    action = 'store_true',
    help   = 'do not generate labels in disassembly',
)
parser.add_argument('-x', '--hexdump',
    action = 'store_true',
    help   = 'show hex in disassembly',
)
parser.add_argument('-s', '--smooth',
    action = 'store_true',
    help   = 'enable smooth rendering mode',
)

args = parser.parse_args()

if args.source:
    result = chipgr8.assemble(inPath=args.source, outPath=args.out)
    if not args.out:
        print(result)
elif args.binary:
    result = chipgr8.disassemble(
        inPath  = chipgr8.findRom(args.binary), 
        outPath = args.out, 
        labels  = None if args.nolabels else {},
        hexdump = args.hexdump,
    )
    if not args.out:
        print(result)
else:
    if not args.rom:
        args.rom = "404.ch8"
    chipgr8.init(
        verbose = args.verbose,
        smooth  = args.smooth,
        ROM     = chipgr8.findRom(args.rom) or "404.ch8", 
        display = True,
    )