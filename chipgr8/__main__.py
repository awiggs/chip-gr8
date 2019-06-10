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
    print("Starting up Chip Gr8 with ", args.rom)
elif args.aInOut:
    chipgr8.assemble(inPath=args.aInOut[0], outPath=args.aInOut[1])
    print("Assemble with:\n\tinputSrcFile: " + args.aInOut[0] + "\n\toutputRomFile: " + args.aInOut[1])
    sys.exit(0)
elif args.dInOut:
    chipgr8.disassemble(inPath=args.dInOut[0], outPath=args.dInOut[1])
    print("disassemble with:\n\tinputRomFile: " + args.dInOut[0] + "\n\toutputSrcFile: " + args.dInOut[1])
    sys.exit(0)

chipgr8.init(args.verbosity, ROM=args.rom, display=True)
