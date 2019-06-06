import chipgr8
import argparse
import sys

def romExists(rom):
    return True

'''
#TODO 

Parse command line arguments and provide the appropriate options to init. 
Possible interface could look like.

usage: chipgr8 
    -v --version The version number
    -h --help    A help message
    -r --rom     The path or name of a rom
'''


# Parse command line arguments and pass appropriate parameters to init
parser = argparse.ArgumentParser(allow_abbrev=False, description="ChipGr8: The AI focused Chip 8 Emulator")
parser.add_argument("-v", "--version", action="store_true", default=False, dest="version", help="display version information and then exit")
parser.add_argument("-vvv", "--verbose", action="store_true", default=False, dest="verbosity", help="show more information on the console while running")
parser.add_argument("-r", "--rom", action="store", dest="rom", default=False, help="provide a chip 8 rom to run")
parser.add_argument("-a", "--assemble", nargs=2, dest="aInOut", help="Run the assembler with in input SRC and output ROM")
parser.add_argument("-d", "--disassemble", nargs=2, dest="dInOut", help="Run the disassembler with in input ROM and output SRC")


args = parser.parse_args()

if args.version:
    print("---VERSION INFO---")
    sys.exit(0)
if args.rom:
    if(not romExists(args.rom)):
        print(args.rom + " is not a valid ROM")
    else:
        print("Starting up Chip Gr8 with ", args.rom)
elif args.aInOut:
    print("Assemble with:\n\tinputSrcFile: " + args.aInOut[0] + "\n\toutputRomFile: " + args.aInOut[1])
elif args.dInOut:
    print("disassemble with:\n\tinputRomFile: " + args.dInOut[0] + "\n\toutputSrcFile: " + args.dInOut[1])

chipgr8.init(args.verbosity, args.rom)